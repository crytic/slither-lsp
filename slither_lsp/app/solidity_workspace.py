import os
import time
import uuid
from dataclasses import dataclass
from time import sleep
from typing import Iterable, Set, List, Dict, Optional

from slither_lsp.app.types.compilation_structures import CompilationTarget
from slither_lsp.lsp.request_handlers.workspace.did_change_watched_files import DidChangeWatchedFilesHandler
from slither_lsp.lsp.requests.client.register_capability import RegisterCapabilityRequest
from slither_lsp.lsp.requests.client.unregister_capability import UnregisterCapabilityRequest
from slither_lsp.lsp.types.basic_structures import WorkspaceFolder, TextDocumentItem
from slither_lsp.lsp.types.params import InitializeResult, InitializeParams, DidChangeWorkspaceFoldersParams, \
    DidOpenTextDocumentParams, DidCloseTextDocumentParams, DidSaveTextDocumentParams, CreateFilesParams, \
    RenameFilesParams, DeleteFilesParams, RegistrationParams, DidChangeWatchedFilesParams, DidChangeTextDocumentParams
from slither_lsp.lsp.types.registration_options import DidChangeWatchedFilesRegistrationOptions, FileSystemWatcher


@dataclass
class SolidityFile:
    """
    Describes a Solidity file, it's dependencies, and any version pragma it has.
    """
    path: str


class SolidityWorkspace:
    """
    Provides a set of methods for tracking and managing Solidity files in a workspace.
    """
    _FILE_CHANGE_POLLING_INTERVAL_SECONDS = 0.2
    _FILE_CHANGE_ANALYSIS_DELAY_SECONDS = 1

    def __init__(self, app):
        # Late import to avoid circular reference issues
        from slither_lsp.app.app import SlitherLSPApp

        # Set our main parameters.
        self.app: SlitherLSPApp = app
        self._init_params: Optional[InitializeParams] = None
        self._shutdown: bool = False

        # Define our workspace parameters.
        self.watch_files_registration_id = str(uuid.uuid4())  # obtain a random uuid for our registration id.
        self.workspace_folders: Dict[str, WorkspaceFolder] = {}
        self.open_text_documents: Dict[str, TextDocumentItem] = {}

        # Define our analysis variables
        self.analysis_last_change_time: float = 0
        self.analysis_pending: bool = False

        # Register our event handlers. Some are registered synchronously so as not to waste resources spinning up
        # a thread. This is fine so long as we do not hang up the thread for long. Any potentially longer running
        # event handlers should be run asynchronously.
        self.app.server.event_emitter.on(
            'server.initialized',
            self.on_server_initialized,
            asynchronous=False
        )
        self.app.server.event_emitter.on(
            'client.initialized',
            self.main_loop,
            asynchronous=True
        )
        self.app.server.event_emitter.on(
            'workspace.didChangeWorkspaceFolders',
            self.on_did_change_workspace_folders,
            asynchronous=False
        )
        self.app.server.event_emitter.on(
            'workspace.didChangeWatchedFiles',
            self.on_did_change_watched_files,
            asynchronous=False
        )
        self.app.server.event_emitter.on(
            'textDocument.didOpen',
            self.on_did_open_text_document,
            asynchronous=False
        )
        self.app.server.event_emitter.on(
            'textDocument.didClose',
            self.on_did_close_text_document,
            asynchronous=False
        )
        self.app.server.event_emitter.on(
            'textDocument.didChange',
            self.on_did_close_text_document,
            asynchronous=False
        )

    def main_loop(self) -> None:
        """
        Runs the main loop, updating state of the Solidity workspace continuously.. This stops executing when
        shutdown() is called, or when the language server receives a shutdown request.
        :return: None
        """
        # Register for our file watching operations on Solidity files.
        RegisterCapabilityRequest.send(
            context=self.app.server.context,
            params=RegistrationParams(
                registrations=[
                    DidChangeWatchedFilesHandler.get_registration(
                        context=self.app.server.context,
                        registration_id=self.watch_files_registration_id,
                        registration_options=DidChangeWatchedFilesRegistrationOptions([
                            FileSystemWatcher(glob_pattern='**/*.sol', kind=None)
                        ])
                    )
                ]
            )
        )

        # Loop while a shutdown was not signalled.
        while not self.shutdown and not self.app.server.context.shutdown:
            if self.analysis_pending:
                if time.time() - self.analysis_last_change_time > self._FILE_CHANGE_ANALYSIS_DELAY_SECONDS:
                    # TODO: Perform new analysis.
                    self.analysis_pending = False

            # Sleep for our polling interval before trying again.
            sleep(self._FILE_CHANGE_POLLING_INTERVAL_SECONDS)

    def shutdown(self):
        """
        Signals that this workspace object should shutdown.
        :return:
        """
        self._shutdown = True

    def on_server_initialized(self, params: InitializeParams, result: InitializeResult) -> None:
        """
        Sets initial data when the server is spun up, such as workspace folders.
        :param params: The client's initialization parameters.
        :param result: The server response to the client's initialization parameters.
        :return: None
        """
        # Set our workspace folder on initialization.
        self._init_params = params
        self.workspace_folders = {
            workspace_folder.uri: workspace_folder for workspace_folder in self._init_params.workspace_folders
        }
        self.open_text_documents = {}

    def on_did_change_workspace_folders(self, params: DidChangeWorkspaceFoldersParams) -> None:
        """
        Applies client-reported changes to the workspace folders.
        :param params: The client's workspace change message parameters.
        :return: None
        """
        # Apply changes to workspace folders.
        for added in params.event.added:
            self.workspace_folders[added.uri] = added
        for removed in params.event.removed:
            self.workspace_folders.pop(removed.uri)

    def on_did_open_text_document(self, params: DidOpenTextDocumentParams) -> None:
        """
        Applies changes to the workspace state as a new file was opened.
        :param params: The client's text document opened message parameters.
        :return: None
        """
        self.open_text_documents[params.text_document.uri] = params.text_document

    def on_did_close_text_document(self, params: DidCloseTextDocumentParams) -> None:
        """
        Applies changes to the workspace state as an opened file was closed.
        :param params: The client's text document closed message parameters.
        :return: None
        """
        self.open_text_documents.pop(params.text_document.uri)

    def on_did_change_text_document(self, params: DidChangeTextDocumentParams) -> None:
        """
        Applies changes to the workspace state as an opened file was changed.
        :param params: The client's text document closed message parameters.
        :return: None
        """
        # TODO: This should invalidate some analysis in this file until it is saved and re-analysis occurs.
        pass

    def on_did_change_watched_files(self, params: DidChangeWatchedFilesParams) -> None:
        """
        Applies changes to the workspace state as files were changed.
        :param params: The client's watched file change parameters.
        :return: None
        """
        # Set our analysis pending status to signal for reanalysis.
        self.analysis_last_change_time = time.time()
        self.analysis_pending = True


def get_solidity_files(folders: Iterable[str], recursive=True) -> Set[str]:
    """
    Loops through all provided folders and obtains a list of all solidity files existing in them.
    This skips 'node_module' folders created by npm/yarn.
    :param folders: A list of folders to search for Solidity files within.
    :param recursive: Indicates if the search for Solidity files should be recursive.
    :return: A list of Solidity file paths which were discovered in the provided folders.
    """
    # Create our resulting set
    solidity_files = set()
    for folder in folders:
        for root, dirs, files in os.walk(folder):
            # Loop through all files and determine if any have a .sol extension
            for file in files:
                filename_base, file_extension = os.path.splitext(file)
                if file_extension is not None and file_extension.lower() == '.sol':
                    solidity_files.add(os.path.join(root, file))

            # If recursive, join our set with any other discovered files in subdirectories.
            if recursive:
                solidity_files.update(
                    get_solidity_files([os.path.join(root, d) for d in dirs], recursive)
                )

    # Return all discovered solidity files
    return solidity_files


def generate_compilation_targets(workspace_folders: List[WorkspaceFolder]) -> List[CompilationTarget]:
    # Get a list of all solidity files in our folders
    #files.update(get_solidity_files(folders))

    # Create our standard json result
    result = {
        'language': 'Solidity',
        'sources': {
            'c:\\contract.sol': {
                'urls': [
                    'c:\\contract.sol'
                ]
            }
        },
        'settings': {
            'remappings': [],
            'optimizer': {
                'enabled': False,
            },
            'outputSelection': {
                '*': {
                    '*': [
                        'abi',
                        'metadata',
                        'devdoc',
                        'userdoc',
                        'evm.bytecode',
                        'evm.deployedBytecode'
                    ],
                    '': [
                        'ast'
                    ]
                }
            }
        }
    }

    # TODO: Parse import strings, create remappings for unresolved imports.
    # Regex: import\s+[^"]*"([^"]+)".*;

    # TODO: Parse semvers, find incompatibilities, put them into different compilation buckets
    #  and potentially return data about satisfactory solc versions, which may enable us to
    #  use solc-select to compile all.
    # Regex: pragma\s+solidity\s+(.*);
