import logging
import os
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor, wait
from dataclasses import dataclass
from functools import lru_cache
from threading import Lock
from time import sleep
from typing import (
    Callable,
    Dict,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeAlias,
)

import lsprotocol.types as lsp
from crytic_compile.crytic_compile import CryticCompile
from crytic_compile.platform.solc_standard_json import SolcStandardJson
from pygls.lsp import METHOD_TO_OPTIONS
from pygls.protocol import LanguageServerProtocol
from pygls.server import LanguageServer
from slither import Slither
from slither.__main__ import (
    _process as process_detectors_and_printers,
)
from slither.__main__ import (
    get_detectors_and_printers,
)
from slither.core.declarations import Contract, Function
from slither.core.source_mapping.source_mapping import Source
from slither.slithir.operations import HighLevelCall, InternalCall
from slither.utils.source_mapping import get_definition
from slither_lsp.app.request_handlers import (
    register_on_goto_implementation,
    register_on_goto_definition,
    register_on_find_references,
)

from slither_lsp.app.feature_analyses.slither_diagnostics import SlitherDiagnostics
from slither_lsp.app.types.analysis_structures import (
    AnalysisResult,
    CompilationTarget,
    CompilationTargetBasic,
    CompilationTargetType,
    SlitherDetectorResult,
    SlitherDetectorSettings,
)
from slither_lsp.app.types.params import (
    ANALYSIS_REPORT_ANALYSIS_PROGRESS,
    COMPILATION_SET_COMPILATION_TARGETS,
    METHOD_TO_TYPES,
    SLITHER_SET_DETECTOR_SETTINGS,
    AnalysisProgressParams,
    AnalysisResultProgress,
    SetCompilationTargetsParams,
)
from slither_lsp.app.utils.file_paths import (
    fs_path_to_uri,
    get_solidity_files,
    is_solidity_file,
    normalize_uri,
    uri_to_fs_path,
)
from slither_lsp.app.utils.ranges import (
    get_object_name_range,
    source_to_location,
    source_to_range,
)

# TODO(frabert): Maybe this should be upstreamed? https://github.com/openlawlibrary/pygls/discussions/338
METHOD_TO_OPTIONS[lsp.WORKSPACE_DID_CHANGE_WATCHED_FILES] = (
    lsp.DidChangeWatchedFilesRegistrationOptions
)

# Type definitions for call hierarchy
Pos: TypeAlias = Tuple[int, int]
Range: TypeAlias = Tuple[Pos, Pos]


def to_lsp_pos(pos: Pos) -> lsp.Position:
    return lsp.Position(line=pos[0], character=pos[1])


def to_lsp_range(range: Range) -> lsp.Range:
    return lsp.Range(start=to_lsp_pos(range[0]), end=to_lsp_pos(range[1]))


def to_pos(pos: lsp.Position) -> Pos:
    return (pos.line, pos.character)


def to_range(range: lsp.Range) -> Range:
    return (to_pos(range.start), to_pos(range.end))


@dataclass(frozen=True)
class CallItem:
    name: str
    range: Range
    filename: str
    offset: str


@dataclass(frozen=True)
class TypeItem:
    name: str
    range: Range
    kind: lsp.SymbolKind
    filename: str
    offset: str


class SlitherProtocol(LanguageServerProtocol):
    # See https://github.com/openlawlibrary/pygls/discussions/441

    @lru_cache
    def get_message_type(self, method: str) -> Optional[Type]:
        return METHOD_TO_TYPES.get(method, (None,))[0] or super().get_message_type(
            method
        )

    @lru_cache
    def get_result_type(self, method: str) -> Optional[Type]:
        return METHOD_TO_TYPES.get(method, (None, None))[1] or super().get_result_type(
            method
        )


class SlitherServer(LanguageServer):
    _logger: logging.Logger
    _init_params: Optional[lsp.InitializeParams] = None

    # Define our workspace parameters.
    workspace_folders: Dict[str, lsp.WorkspaceFolder] = {}
    open_text_documents: Dict[str, lsp.TextDocumentItem] = {}

    # Define our analysis variables

    # Define a set of all solidity files available in the workspace which we track with appropriate file events.
    solidity_file_uris: Set[str] = set()
    solidity_files_lock = Lock()  # lock for updating the above
    _solidity_files_scan_required = (
        True  # determines if we need to scan filesystem for all solidity files
    )

    # Define a set of compilation targets which are autogenerated if not user supplied.
    compilation_targets: List[CompilationTarget] = []
    compilation_targets_lock = Lock()  # lock for updating the above
    compilation_targets_autogenerate = True
    compilation_targets_enabled = False

    # Define our compilation variables
    analyses: List[AnalysisResult] = []

    # Define our slither diagnostics provider
    detector_settings: SlitherDetectorSettings = SlitherDetectorSettings(
        enabled=True, hidden_checks=[]
    )
    slither_diagnostics: Optional[SlitherDiagnostics] = None

    refresh_lock = (
        Lock()
    )  # Makes sure at most one refresh operation is in flight at any point in time
    REFRESH_WAIT_SECONDS = 1.0

    analysis_pool = ThreadPoolExecutor()

    def __init__(self, logger: logging.Logger, *args):
        super().__init__(protocol_cls=SlitherProtocol, *args)

        self._logger = logger
        self.slither_diagnostics = SlitherDiagnostics(self)

        @self.feature(lsp.INITIALIZE)
        def on_initialize(ls: SlitherServer, params):
            ls._on_initialize(params)

        @self.feature(lsp.INITIALIZED)
        def on_initialized(ls: SlitherServer, params):
            ls.show_message("slither-lsp initialized", lsp.MessageType.Debug)

        @self.thread()
        @self.feature(
            lsp.WORKSPACE_DID_CHANGE_WATCHED_FILES,
            lsp.DidChangeWatchedFilesRegistrationOptions(
                [lsp.FileSystemWatcher("**/*.sol")]
            ),
        )
        def on_did_change_watched_files(ls: SlitherServer, params):
            ls._on_did_change_watched_files(params)

        @self.thread()
        @self.feature(lsp.WORKSPACE_DID_CHANGE_WORKSPACE_FOLDERS)
        def on_did_change_workspace_folder(ls: SlitherServer, params):
            ls._on_did_change_workspace_folders(params)

        @self.thread()
        @self.feature(lsp.TEXT_DOCUMENT_DID_CLOSE)
        def on_did_close_text_document(ls: SlitherServer, params):
            ls._on_did_close_text_document(params)

        @self.thread()
        @self.feature(lsp.TEXT_DOCUMENT_DID_OPEN)
        def on_text_document_did_open(ls: SlitherServer, params):
            ls._on_did_open_text_document(params)

        @self.thread()
        @self.feature(SLITHER_SET_DETECTOR_SETTINGS)
        def on_set_detector_settings(ls: SlitherServer, params):
            ls._on_set_detector_settings(params)

        @self.thread()
        @self.feature(COMPILATION_SET_COMPILATION_TARGETS)
        def on_set_compilation_targets(ls: SlitherServer, params):
            ls._on_set_compilation_targets(params)

        register_on_goto_definition(self)
        register_on_goto_implementation(self)
        register_on_find_references(self)

        @self.thread()
        @self.feature(lsp.TEXT_DOCUMENT_PREPARE_CALL_HIERARCHY)
        def on_prepare_call_hierarchy(ls: SlitherServer, params):
            return ls._on_prepare_call_hierarchy(params)

        @self.thread()
        @self.feature(lsp.CALL_HIERARCHY_INCOMING_CALLS)
        def on_get_incoming_calls(ls: SlitherServer, params):
            return ls._on_get_incoming_calls(params)

        @self.thread()
        @self.feature(lsp.CALL_HIERARCHY_OUTGOING_CALLS)
        def on_get_outgoing_calls(ls: SlitherServer, params):
            return ls._on_get_outgoing_calls(params)

        @self.thread()
        @self.feature(lsp.TEXT_DOCUMENT_PREPARE_TYPE_HIERARCHY)
        def on_prepare_type_hierarchy(ls: SlitherServer, params):
            return ls._on_prepare_type_hierarchy(params)

        @self.thread()
        @self.feature(lsp.TYPE_HIERARCHY_SUBTYPES)
        def on_get_subtypes(ls: SlitherServer, params):
            return ls._on_get_subtypes(params)

        @self.thread()
        @self.feature(lsp.TYPE_HIERARCHY_SUPERTYPES)
        def on_get_supertypes(ls: SlitherServer, params):
            return ls._on_get_supertypes(params)

    @property
    def workspace_opened(self):
        """
        If True, indicates a workspace folder has been opened.
        If False, no workspace folder is opened and files in opened tabs will be targeted.
        :return: None
        """
        return len(self.workspace_folders) > 0

    def _on_initialize(self, params: lsp.InitializeParams) -> None:
        """
        Sets initial data when the server is spun up, such as workspace folders.
        :param params: The client's initialization parameters.
        :param result: The server response to the client's initialization parameters.
        :return: None
        """
        # Set our workspace folder on initialization.
        self._init_params = params
        self.workspace_folders = {
            workspace_folder.uri: workspace_folder
            for workspace_folder in self._init_params.workspace_folders or []
        }
        self.open_text_documents = {}

    def queue_reanalysis(self, files_rescan: bool = False) -> None:
        """
        Queues all compilation targets for reanalysis.
        :param files_rescan: If True, indicates the list of Solidity files in the workspace will be
        re-evaluated.
        :return: None
        """
        # Update the tracked solidity files in the workspace if requested.
        with self.solidity_files_lock:
            if files_rescan:
                self._solidity_files_scan_required = True

        self.refresh_workspace()

    def _on_did_change_workspace_folders(
        self, params: lsp.DidChangeWorkspaceFoldersParams
    ) -> None:
        """
        Applies client-reported changes to the workspace folders.
        :param params: The client's workspace change message parameters.
        :return: None
        """
        # Apply changes to workspace folders.
        with self.solidity_files_lock:
            for added in params.event.added:
                self.workspace_folders[normalize_uri(added.uri)] = added
            for removed in params.event.removed:
                self.workspace_folders.pop(normalize_uri(removed.uri), None)

        # Trigger a re-scan of the workspace Solidity files and re-analyze the codebase.
        self.queue_reanalysis(files_rescan=True)

    def _on_did_open_text_document(self, params: lsp.DidOpenTextDocumentParams) -> None:
        """
        Applies changes to the workspace state as a new file was opened.
        :param params: The client's text document opened message parameters.
        :return: None
        """
        # Update our open text document lookup.
        self.open_text_documents[normalize_uri(params.text_document.uri)] = (
            params.text_document
        )

        # If we have no workspace folders open, update our solidity files list and re-analyze immediately.
        if not self.workspace_opened:
            self.queue_reanalysis(files_rescan=True)

    def _on_did_close_text_document(
        self, params: lsp.DidCloseTextDocumentParams
    ) -> None:
        """
        Applies changes to the workspace state as an opened file was closed.
        :param params: The client's text document closed message parameters.
        :return: None
        """
        # Update our open text document lookup.
        self.open_text_documents.pop(normalize_uri(params.text_document.uri), None)

        # If we have no workspace folders open, update our solidity files list and re-analyze immediately.
        if not self.workspace_opened:
            self.queue_reanalysis(files_rescan=True)

    def _on_did_change_watched_files(
        self, params: lsp.DidChangeWatchedFilesParams
    ) -> None:
        """
        Applies changes to the workspace state as files were changed.
        :param params: The client's watched file change parameters.
        :return: None
        """
        # Update our solidity file list
        updated_solidity_files = False
        with self.solidity_files_lock:
            for file_event in params.changes:
                target_uri = normalize_uri(file_event.uri)
                if (
                    file_event.type == lsp.FileChangeType.Created
                    or file_event.type == lsp.FileChangeType.Changed
                ):
                    self.solidity_file_uris.add(target_uri)
                elif file_event.type == lsp.FileChangeType.Deleted:
                    self.solidity_file_uris.remove(target_uri)
                updated_solidity_files = updated_solidity_files or is_solidity_file(
                    target_uri
                )

        # Set our analysis pending status to signal for reanalysis.
        if updated_solidity_files:
            self.queue_reanalysis()

    def _on_set_detector_settings(self, params: SlitherDetectorSettings) -> None:
        """
        Sets the detector settings for the workspace, indicating how detector output should be presented.
        :param params: The parameters provided for the set detector settings request.
        :return: None
        """
        # If our detector settings are not different than existing ones, we do not need to trigger any on-change events.
        if params == self.detector_settings:
            return

        # Set our detector settings
        self.detector_settings = params

        # Refresh our detector output
        self._refresh_detector_output()

    def _on_set_compilation_targets(self, params: SetCompilationTargetsParams) -> None:
        """
        Sets the compilation targets for the workspace to use. If empty, auto-compilation will be used instead.
        :param params: The parameters provided for the set compilation request.
        :return: None
        """
        # Update our solidity file list
        with self.compilation_targets_lock:
            # Update our list of compilation targets
            self.compilation_targets = params.targets
            self.compilation_targets_enabled = True
            self.compilation_targets_autogenerate = len(self.compilation_targets) == 0

        # Set our analysis pending status to signal for reanalysis.
        self.queue_reanalysis(files_rescan=True)

    def _report_compilation_progress(self) -> None:
        """
        Reports current analysis progress to the client.
        :return: None
        """
        # Create a list of progress reports for each analysis result.
        report_progress_params_results: List[AnalysisResultProgress] = []

        # Report on progress for each compilation target
        for compilation_target in self.compilation_targets:
            # See if we can find a corresponding analysis.
            corresponding_analysis: Optional[AnalysisResult] = None
            for analysis in self.analyses:
                if analysis.compilation_target == compilation_target:
                    corresponding_analysis = analysis

            # Add progress for this compilation target
            report_progress_params_results.append(
                AnalysisResultProgress(
                    succeeded=(
                        None
                        if corresponding_analysis is None
                        else corresponding_analysis.succeeded
                    ),
                    compilation_target=compilation_target,
                    error=(
                        None
                        if corresponding_analysis is None
                        or corresponding_analysis.error is None
                        else str(corresponding_analysis.error)
                    ),
                )
            )

        # Send the reports to the client.
        report_progress_params = AnalysisProgressParams(
            results=report_progress_params_results
        )
        self.send_notification(
            ANALYSIS_REPORT_ANALYSIS_PROGRESS, report_progress_params
        )

    def _refresh_detector_output(self):
        """
        Refreshes language server state given new analyses output or detector settings.
        :return: None
        """
        # Update our diagnostics with new detector output.
        self.slither_diagnostics.update(self.analyses, self.detector_settings)

    def refresh_workspace(self) -> None:
        """
        Refreshes the currently opened workspace state, tracking new files if a workspace change occurred, re-running
        compilation and analysis if needed, and refreshing analysis output such as for slither detectors.
        :return:
        """
        detector_classes, _ = get_detectors_and_printers()

        def analyze(compilation_target: CompilationTarget):
            analyzed_successfully = True
            compilation: Optional[CryticCompile] = None
            analysis = None
            analysis_error = None
            detector_results = None
            try:
                self._logger.info(
                    "Started compiling %s",
                    compilation_target.target_basic.target,
                )
                # Compile our target
                compilation = self._compile_target(compilation_target)

                # Create our analysis.
                analysis = Slither(compilation)

                # Run detectors and obtain results
                self._logger.info(
                    "Processing %s", compilation_target.target_basic.target
                )
                _, detector_results, _, _ = process_detectors_and_printers(
                    analysis, detector_classes, []
                )
                # Parse detector results
                if detector_results is not None and isinstance(detector_results, list):
                    detector_results = [
                        SlitherDetectorResult.from_dict(detector_result)
                        for detector_result in detector_results
                    ]
                else:
                    detector_results = None

            except Exception as err:
                self._logger.error(
                    "Failed compiling %s: %s",
                    compilation_target.target_basic.target,
                    err,
                )
                # If we encounter an error, set our status.
                analyzed_successfully = False
                analysis_error = err

            self._logger.info(
                "Done compiling %s", compilation_target.target_basic.target
            )

            # Add our analysis
            self.analyses.append(
                AnalysisResult(
                    succeeded=analyzed_successfully,
                    compilation_target=compilation_target,
                    compilation=compilation,
                    analysis=analysis,
                    error=analysis_error,
                    detector_results=detector_results,
                )
            )

            # Report analysis status to our client
            self._report_compilation_progress()

        def start_refresh():
            # Gives a chance to the main thread to update the compilation targets before starting
            sleep(self.REFRESH_WAIT_SECONDS)

            with self.refresh_lock:
                targets_copy = []
                with self.compilation_targets_lock:
                    targets_copy = self.compilation_targets.copy()

                futures = [
                    self.analysis_pool.submit(analyze, target)
                    for target in targets_copy
                ]
                wait(futures)

                # Refresh our detector results
                self._refresh_detector_output()

        # First refresh our initial solidity target list for this workspace
        with self.solidity_files_lock:
            # If we're meant to re-scan our solidity files, do so to get an initial collection of solidity target
            # locations. This can happen on initialization or workspace folder change.
            if self._solidity_files_scan_required:
                # If we have no workspace folders, we'll instead use our open text documents as targets.
                if not self.workspace_opened:
                    self.solidity_file_uris = set(
                        [
                            open_doc.uri
                            for open_doc in self.open_text_documents.values()
                            if is_solidity_file(open_doc.uri)
                        ]
                    )
                else:
                    solidity_file_paths = get_solidity_files(
                        [
                            uri_to_fs_path(workspace_folder.uri)
                            for workspace_folder in self.workspace_folders.values()
                        ]
                    )
                    self.solidity_file_uris = set(
                        [fs_path_to_uri(fspath) for fspath in solidity_file_paths]
                    )
                self._solidity_files_scan_required = False

            # Regenerate new compilation targets if desired.
            with self.compilation_targets_lock:
                if self.compilation_targets_autogenerate:
                    self.compilation_targets = self.generate_compilation_targets()

        self.analysis_pool.submit(start_refresh)

    def generate_compilation_targets(self) -> List[CompilationTarget]:
        # TODO: Loop through self.solidity_files, parse files to determine which compilation buckets/parameters
        #  should be used.

        # TODO: Parse import strings, create remappings for unresolved imports.
        # Regex: import\s+[^"]*"([^"]+)".*;

        # TODO: Parse semvers, find incompatibilities, put them into different compilation buckets
        #  and potentially return data about satisfactory solc versions, which may enable us to
        #  use solc-select to compile all.
        # Regex: pragma\s+solidity\s+(.*);

        file_paths = map(uri_to_fs_path, self.solidity_file_uris)
        workspaces = map(uri_to_fs_path, self.workspace_folders)
        targets = map(
            lambda path: CompilationTarget(
                target_type=CompilationTargetType.BASIC,
                target_basic=CompilationTargetBasic(path),
                cwd_workspace=next(
                    filter(
                        lambda folder: os.path.commonprefix([path, folder]) == folder,
                        workspaces,
                    ),
                    None,
                ),
                crytic_compile_args=None,
            ),
            file_paths,
        )

        return list(targets)

    def _compile_target(self, compilation_settings: CompilationTarget) -> CryticCompile:
        """
        Compiles a target with the provided compilation settings using crytic-compile.
        :return: Returns an instance of crytic-compile.
        """
        if compilation_settings.target_type == CompilationTargetType.BASIC:
            # If the target type is a basic target and we have provided settings, pass them to crytic compile.
            if compilation_settings.target_basic is not None:
                # Obtain our workspace folder
                workspace_folder_path: Optional[str] = None
                if compilation_settings.cwd_workspace is not None:
                    for workspace_folder in self.workspace_folders.values():
                        if (
                            workspace_folder.name.lower()
                            == compilation_settings.cwd_workspace.lower()
                        ):
                            workspace_folder_path = uri_to_fs_path(workspace_folder.uri)
                            break

                # Obtain our target. If this is a relative path, we prepend our working directory.
                target_path = compilation_settings.target_basic.target
                if not os.path.isabs(target_path) and workspace_folder_path is not None:
                    target_path = os.path.normpath(
                        os.path.join(workspace_folder_path, target_path)
                    )

                # Compile our target
                return CryticCompile(
                    target_path, cwd=compilation_settings.cwd_workspace
                )

        elif compilation_settings.target_type == CompilationTargetType.STANDARD_JSON:
            # If the target type is standard json and we have provided settings, pass them to crytic compile.
            if compilation_settings.target_standard_json is not None:
                # TODO: Add support for other arguments (solc_working_dir, etc)
                return CryticCompile(
                    SolcStandardJson(compilation_settings.target_standard_json.target)
                )

        # Raise an exception if there was no relevant exception.
        raise ValueError(
            f"Could not compile target type {compilation_settings.target_type.name} as insufficient settings were "
            f"provided."
        )

    def _get_analyses_containing(
        self, filename: str
    ) -> List[Tuple[Slither, CryticCompile]]:
        def lookup(comp):
            try:
                return comp.filename_lookup(filename)
            except ValueError:
                return None

        return [
            (analysis_result.analysis, analysis_result.compilation)
            for analysis_result in self.analyses.copy()
            if analysis_result.analysis is not None
            and lookup(analysis_result.compilation) is not None
        ]

    def _on_prepare_call_hierarchy(
        self, params: lsp.CallHierarchyPrepareParams
    ) -> Optional[List[lsp.CallHierarchyItem]]:
        """
        `textDocument/prepareCallHierarchy` doesn't actually produce
        the call hierarchy in this case, it only detects what objects
        we are trying to produce the call hierarchy for.
        The data returned from this method will be sent by the client
        back to the "get incoming/outgoing calls" later.
        """
        res: Dict[Tuple[str, int], lsp.CallHierarchyItem] = {}

        # Obtain our filename for this file
        target_filename_str: str = uri_to_fs_path(params.text_document.uri)

        for analysis, comp in self._get_analyses_containing(target_filename_str):
            # Obtain the offset for this line + character position
            target_offset = comp.get_global_offset_from_line(
                target_filename_str, params.position.line + 1
            )
            # Obtain objects
            objects = analysis.offset_to_objects(
                target_filename_str, target_offset + params.position.character
            )
            for obj in objects:
                source = obj.source_mapping
                if not isinstance(obj, Function):
                    continue
                offset = get_definition(obj, comp).start
                res[(target_filename_str, offset)] = lsp.CallHierarchyItem(
                    name=obj.canonical_name,
                    kind=lsp.SymbolKind.Function,
                    uri=fs_path_to_uri(source.filename.absolute),
                    range=source_to_range(source),
                    selection_range=get_object_name_range(obj, comp),
                    data={
                        "filename": target_filename_str,
                        "offset": offset,
                    },
                )
        return [elem for elem in res.values()]

    def _on_get_incoming_calls(
        self, params: lsp.CallHierarchyIncomingCallsParams
    ) -> Optional[List[lsp.CallHierarchyIncomingCall]]:
        res: Dict[CallItem, Set[Range]] = defaultdict(set)

        # Obtain our filename for this file
        # These will have been populated either by
        # the initial "prepare call hierarchy" or by
        # other calls to "get incoming calls"
        target_filename_str = params.item.data["filename"]
        target_offset = params.item.data["offset"]

        # According to https://docs.python.org/3/faq/library.html#what-kinds-of-global-value-mutation-are-thread-safe
        # there's no need to acquire a lock here
        analyses_copy = self.analyses.copy()

        referenced_functions = [
            obj
            for analysis, comp in self._get_analyses_containing(target_filename_str)
            for obj in analysis.offset_to_objects(target_filename_str, target_offset)
            if isinstance(obj, Function)
        ]

        calls = [
            (f, op, analysis_result.compilation)
            for analysis_result in analyses_copy
            if analysis_result.analysis is not None
            for comp_unit in analysis_result.analysis.compilation_units
            for f in comp_unit.functions
            for op in f.all_slithir_operations()
            if isinstance(op, (InternalCall, HighLevelCall))
            and isinstance(op.function, Function)
        ]

        for func in referenced_functions:
            for call_from, call, call_comp in calls:
                # TODO(frabert): Ideally we'd do this instead, but apparently the same function may be represented by multiple objects in Slither
                # if call.function is not func:
                #     continue

                if call.function.canonical_name != func.canonical_name:
                    continue
                expr_range = source_to_range(call.expression.source_mapping)
                func_range = source_to_range(call_from.source_mapping)
                item = CallItem(
                    name=call_from.canonical_name,
                    range=to_range(func_range),
                    filename=call_from.source_mapping.filename.absolute,
                    offset=get_definition(call_from, call_comp).start,
                )
                res[item].add(to_range(expr_range))
        return [
            lsp.CallHierarchyIncomingCall(
                from_=lsp.CallHierarchyItem(
                    name=call_from.name,
                    kind=lsp.SymbolKind.Function,
                    uri=fs_path_to_uri(call_from.filename),
                    range=to_lsp_range(call_from.range),
                    selection_range=to_lsp_range(call_from.range),
                    data={
                        "filename": call_from.filename,
                        "offset": call_from.offset,
                    },
                ),
                from_ranges=[to_lsp_range(range) for range in ranges],
            )
            for (call_from, ranges) in res.items()
        ]

    def _on_get_outgoing_calls(
        self, params: lsp.CallHierarchyOutgoingCallsParams
    ) -> Optional[List[lsp.CallHierarchyOutgoingCall]]:
        res: Dict[CallItem, Set[Range]] = defaultdict(set)

        # Obtain our filename for this file
        target_filename_str = params.item.data["filename"]
        target_offset = params.item.data["offset"]

        for analysis, comp in self._get_analyses_containing(target_filename_str):
            objects = analysis.offset_to_objects(target_filename_str, target_offset)
            for obj in objects:
                if not isinstance(obj, Function):
                    continue
                calls = [
                    op
                    for op in obj.all_slithir_operations()
                    if isinstance(op, (InternalCall, HighLevelCall))
                ]
                for call in calls:
                    if not isinstance(call.function, Function):
                        continue
                    call_to = call.function
                    expr_range = source_to_range(call.expression.source_mapping)
                    func_range = source_to_range(call_to.source_mapping)
                    item = CallItem(
                        name=call_to.canonical_name,
                        range=to_range(func_range),
                        filename=call_to.source_mapping.filename.absolute,
                        offset=get_definition(call_to, comp).start,
                    )
                    res[item].add(to_range(expr_range))

        return [
            lsp.CallHierarchyOutgoingCall(
                to=lsp.CallHierarchyItem(
                    name=call_to.name,
                    kind=lsp.SymbolKind.Function,
                    uri=fs_path_to_uri(call_to.filename),
                    range=to_lsp_range(call_to.range),
                    selection_range=to_lsp_range(call_to.range),
                    data={
                        "filename": call_to.filename,
                        "offset": call_to.offset,
                    },
                ),
                from_ranges=[to_lsp_range(range) for range in ranges],
            )
            for (call_to, ranges) in res.items()
        ]

    def _on_prepare_type_hierarchy(
        self, params: lsp.TypeHierarchyPrepareParams
    ) -> Optional[List[lsp.TypeHierarchyItem]]:
        res: Set[TypeItem] = set()

        # Obtain our filename for this file
        target_filename_str: str = uri_to_fs_path(params.text_document.uri)

        for analysis, comp in self._get_analyses_containing(target_filename_str):
            # Obtain the offset for this line + character position
            target_offset = comp.get_global_offset_from_line(
                target_filename_str, params.position.line + 1
            )
            # Obtain objects
            objects = analysis.offset_to_objects(
                target_filename_str, target_offset + params.position.character
            )
            for obj in objects:
                source = obj.source_mapping
                if not isinstance(obj, Contract):
                    continue
                offset = get_definition(obj, comp).start
                range = get_object_name_range(obj, comp)
                if obj.is_interface:
                    kind = lsp.SymbolKind.Interface
                else:
                    kind = lsp.SymbolKind.Class
                res.add(
                    TypeItem(
                        name=obj.name,
                        range=to_range(range),
                        kind=kind,
                        filename=source.filename.absolute,
                        offset=offset,
                    )
                )
        return [
            lsp.TypeHierarchyItem(
                name=item.name,
                kind=item.kind,
                uri=fs_path_to_uri(item.filename),
                range=to_lsp_range(item.range),
                selection_range=to_lsp_range(item.range),
                data={
                    "filename": item.filename,
                    "offset": item.offset,
                },
            )
            for item in res
        ]

    def _on_get_subtypes(
        self, params: lsp.TypeHierarchySubtypesParams
    ) -> Optional[List[lsp.TypeHierarchyItem]]:
        res: Set[TypeItem] = set()

        # Obtain our filename for this file
        # These will have been populated either by
        # the initial "prepare call hierarchy" or by
        # other calls to "get incoming calls"
        target_filename_str = params.item.data["filename"]
        target_offset = params.item.data["offset"]

        referenced_contracts = [
            contract
            for analysis, _ in self._get_analyses_containing(target_filename_str)
            for contract in analysis.offset_to_objects(
                target_filename_str, target_offset
            )
            if isinstance(contract, Contract)
        ]

        contracts = [
            (contract, analysis_result.compilation)
            for analysis_result in self.analyses.copy()
            if analysis_result.analysis is not None
            for comp_unit in analysis_result.analysis.compilation_units
            for contract in comp_unit.contracts
        ]

        for contract in referenced_contracts:
            for other_contract, other_contract_comp in contracts:
                if contract not in other_contract.immediate_inheritance:
                    continue
                range = get_object_name_range(other_contract, other_contract_comp)
                if other_contract.is_interface:
                    kind = lsp.SymbolKind.Interface
                else:
                    kind = lsp.SymbolKind.Class
                item = TypeItem(
                    name=other_contract.name,
                    range=to_range(range),
                    kind=kind,
                    filename=other_contract.source_mapping.filename.absolute,
                    offset=get_definition(other_contract, other_contract_comp).start,
                )
                res.add(item)
        return [
            lsp.TypeHierarchyItem(
                name=item.name,
                kind=item.kind,
                uri=fs_path_to_uri(item.filename),
                range=to_lsp_range(item.range),
                selection_range=to_lsp_range(item.range),
                data={
                    "filename": item.filename,
                    "offset": item.offset,
                },
            )
            for item in res
        ]

    def _on_get_supertypes(
        self, params: lsp.TypeHierarchySupertypesParams
    ) -> Optional[List[lsp.TypeHierarchyItem]]:
        res: Set[TypeItem] = set()

        # Obtain our filename for this file
        # These will have been populated either by
        # the initial "prepare call hierarchy" or by
        # other calls to "get incoming calls"
        target_filename_str = params.item.data["filename"]
        target_offset = params.item.data["offset"]

        supertypes = [
            (supertype, comp)
            for analysis, comp in self._get_analyses_containing(target_filename_str)
            for contract in analysis.offset_to_objects(
                target_filename_str, target_offset
            )
            if isinstance(contract, Contract)
            for supertype in contract.immediate_inheritance
        ]

        for sup, comp in supertypes:
            range = get_object_name_range(sup, comp)
            if sup.is_interface:
                kind = lsp.SymbolKind.Interface
            else:
                kind = lsp.SymbolKind.Class
            item = TypeItem(
                name=sup.name,
                range=to_range(range),
                kind=kind,
                filename=sup.source_mapping.filename.absolute,
                offset=get_definition(sup, comp).start,
            )
            res.add(item)
        return [
            lsp.TypeHierarchyItem(
                name=item.name,
                kind=item.kind,
                uri=fs_path_to_uri(item.filename),
                range=to_lsp_range(item.range),
                selection_range=to_lsp_range(item.range),
                data={
                    "filename": item.filename,
                    "offset": item.offset,
                },
            )
            for item in res
        ]
