import logging
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from threading import Lock
from typing import Dict, List, Optional, Tuple, Type
from os.path import split

import lsprotocol.types as lsp
from crytic_compile.crytic_compile import CryticCompile
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

from slither_lsp.app.feature_analyses.slither_diagnostics import SlitherDiagnostics
from slither_lsp.app.logging import LSPHandler
from slither_lsp.app.request_handlers import (
    register_on_find_references,
    register_on_get_incoming_calls,
    register_on_get_outgoing_calls,
    register_on_get_subtypes,
    register_on_get_supertypes,
    register_on_goto_definition,
    register_on_goto_implementation,
    register_on_prepare_call_hierarchy,
    register_on_prepare_type_hierarchy,
    register_inlay_hints_handlers,
    register_symbols_handlers,
)
from slither_lsp.app.types.analysis_structures import (
    AnalysisResult,
    SlitherDetectorResult,
    SlitherDetectorSettings,
)
from slither_lsp.app.types.params import (
    METHOD_TO_TYPES,
    SLITHER_SET_DETECTOR_SETTINGS,
    SLITHER_ANALYZE,
    AnalysisRequestParams,
)
from slither_lsp.app.utils.file_paths import normalize_uri, uri_to_fs_path

# TODO(frabert): Maybe this should be upstreamed? https://github.com/openlawlibrary/pygls/discussions/338
METHOD_TO_OPTIONS[lsp.WORKSPACE_DID_CHANGE_WATCHED_FILES] = (
    lsp.DidChangeWatchedFilesRegistrationOptions
)


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
    workspaces: Dict[str, AnalysisResult] = {}
    # `workspace_in_progress[uri]` is locked if there's a compilation in progress for the workspace `uri`
    workspace_in_progress: Dict[str, Lock] = defaultdict(Lock)

    @property
    def analyses(self) -> List[AnalysisResult]:
        return list(self.workspaces.values())

    # Define our slither diagnostics provider
    detector_settings: SlitherDetectorSettings = SlitherDetectorSettings(
        enabled=True, hidden_checks=[]
    )

    analysis_pool = ThreadPoolExecutor()

    def __init__(self, logger: logging.Logger, *args):
        super().__init__(protocol_cls=SlitherProtocol, *args)

        self._logger = logger
        self._logger.addHandler(LSPHandler(self))
        self.slither_diagnostics = SlitherDiagnostics(self)

        @self.feature(lsp.INITIALIZE)
        def on_initialize(ls: SlitherServer, params):
            ls._on_initialize(params)

        @self.feature(lsp.INITIALIZED)
        def on_initialized(ls: SlitherServer, params):
            ls.show_message("slither-lsp initialized", lsp.MessageType.Debug)

        @self.thread()
        @self.feature(lsp.WORKSPACE_DID_CHANGE_WORKSPACE_FOLDERS)
        def on_did_change_workspace_folder(ls: SlitherServer, params):
            ls._on_did_change_workspace_folders(params)

        @self.thread()
        @self.feature(SLITHER_SET_DETECTOR_SETTINGS)
        def on_set_detector_settings(ls: SlitherServer, params):
            ls._on_set_detector_settings(params)

        @self.thread()
        @self.feature(SLITHER_ANALYZE)
        def on_analyze(ls: SlitherServer, params):
            ls._on_analyze(params)

        register_on_goto_definition(self)
        register_on_goto_implementation(self)
        register_on_find_references(self)

        register_on_prepare_call_hierarchy(self)
        register_on_get_incoming_calls(self)
        register_on_get_outgoing_calls(self)

        register_on_prepare_type_hierarchy(self)
        register_on_get_subtypes(self)
        register_on_get_supertypes(self)

        register_inlay_hints_handlers(self)

        register_symbols_handlers(self)

    @property
    def workspace_opened(self):
        """
        If True, indicates a workspace folder has been opened.
        If False, no workspace folder is opened and files in opened tabs will be targeted.
        :return: None
        """
        return len(self.workspaces.items()) > 0

    def _on_initialize(self, params: lsp.InitializeParams) -> None:
        """
        Sets initial data when the server is spun up, such as workspace folders.
        :param params: The client's initialization parameters.
        :param result: The server response to the client's initialization parameters.
        :return: None
        """
        # Set our workspace folder on initialization.
        self._init_params = params
        for workspace in params.workspace_folders or []:
            self.queue_compile_workspace(normalize_uri(workspace.uri))

    def _on_analyze(self, params: AnalysisRequestParams):
        uris = [normalize_uri(uri) for uri in params.uris or self.workspaces.keys()]
        for uri in uris:
            path = uri_to_fs_path(uri)
            workspace_name = split(path)[1]
            if self.workspace_in_progress[uri].locked():
                self.show_message(
                    f"Analysis for {workspace_name} is already in progress",
                    lsp.MessageType.Warning,
                )
                continue
            self.queue_compile_workspace(uri)

    def queue_compile_workspace(self, uri: str):
        """
        Queues a workspace for compilation. `uri` should be normalized
        """
        path = uri_to_fs_path(uri)
        workspace_name = split(path)[1]

        def compile():
            detector_classes, _ = get_detectors_and_printers()
            with self.workspace_in_progress[uri]:
                self.show_message(
                    f"Compilation for {workspace_name} has started",
                    lsp.MessageType.Info,
                )
                try:
                    compilation = CryticCompile(path)
                    analysis = Slither(compilation)
                    _, detector_results, _, _ = process_detectors_and_printers(
                        analysis, detector_classes, []
                    )
                    # Parse detector results
                    if detector_results is not None and isinstance(
                        detector_results, list
                    ):
                        detector_results = [
                            SlitherDetectorResult.from_dict(detector_result)
                            for detector_result in detector_results
                        ]
                    else:
                        detector_results = None
                    analyzed_successfully = True
                    analysis_error = None
                    self.show_message(
                        f"Compilation for {workspace_name} has completed successfully",
                        lsp.MessageType.Info,
                    )
                except Exception as err:
                    # If we encounter an error, set our status.
                    analysis = None
                    compilation = None
                    analyzed_successfully = False
                    analysis_error = err
                    detector_results = None
                    self.show_message(
                        f"Compilation for {workspace_name} has failed. See log for details.",
                        lsp.MessageType.Info,
                    )
                    self._logger.log(
                        logging.ERROR, "Compiling %s has failed: %s", path, err
                    )

                self.workspaces[uri] = AnalysisResult(
                    succeeded=analyzed_successfully,
                    compilation=compilation,
                    analysis=analysis,
                    error=analysis_error,
                    detector_results=detector_results,
                )
                self._refresh_detector_output()

        self.analysis_pool.submit(compile)

    def _on_did_change_workspace_folders(
        self, params: lsp.DidChangeWorkspaceFoldersParams
    ) -> None:
        """
        Applies client-reported changes to the workspace folders.
        :param params: The client's workspace change message parameters.
        :return: None
        """
        for added in params.event.added:
            uri = normalize_uri(added.uri)
            if not self.workspace_in_progress[uri].locked():
                self.queue_compile_workspace(uri)
        for removed in params.event.removed:
            uri = normalize_uri(removed.uri)
            with self.workspace_in_progress[uri]:
                self.workspaces.pop(uri, None)

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

    def _refresh_detector_output(self):
        """
        Refreshes language server state given new analyses output or detector settings.
        :return: None
        """
        # Update our diagnostics with new detector output.
        self.slither_diagnostics.update(self.analyses, self.detector_settings)

    def get_analyses_containing(
        self, filename: str
    ) -> List[Tuple[Slither, CryticCompile]]:
        def lookup(comp: CryticCompile):
            try:
                return comp.filename_lookup(filename)
            except ValueError:
                return None

        return [
            (analysis_result.analysis, analysis_result.compilation)
            for analysis_result in self.analyses
            if analysis_result.analysis is not None
            and analysis_result.compilation is not None
            and lookup(analysis_result.compilation) is not None
        ]
