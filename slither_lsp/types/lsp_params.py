# pylint: disable=duplicate-code
from dataclasses import dataclass
from typing import Union, Any, Optional, List

from slither_lsp.types.lsp_capabilities import ClientCapabilities, ServerCapabilities
from slither_lsp.types.lsp_basic_structures import ClientServerInfo, TraceValue, WorkspaceFolder, MessageType, Range
from slither_lsp.types.base_serializable_structure import SerializableStructure


@dataclass
class WorkDoneProgressParams(SerializableStructure):
    """
    Data structure which represents a work done progress token.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#workDoneProgressParams
    """
    # An optional token that a server can use to report work done progress.
    work_done_token: Union[str, int, None]

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['work_done_token'] = source_dict.get('workDoneToken')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create a result dictionary if we don't have one and set our fields
        result = result if result is not None else {}
        if self.work_done_token is not None:
            result['workDoneToken'] = self.work_done_token

        # Return the result.
        return result


@dataclass
class InitializeParams(SerializableStructure):
    """
    Data structure which represents 'initialize' request parameters.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#initializeParams
    """
    # The process Id of the parent process that started the server. Is null if
    # the process has not been started by another process. If the parent
    # process is not alive then the server should exit (see exit notification)
    # its process.
    process_id: Optional[int]

    # Information about the client
    client_info: Optional[ClientServerInfo]

    # The locale the client is currently showing the user interface
    # in. This must not necessarily be the locale of the operating
    # system.
    #
    # Uses IETF language tags as the value's syntax
    # (See https://en.wikipedia.org/wiki/IETF_language_tag)
    #
    # @since 3.16.0
    locale: Optional[str]

    # The rootPath of the workspace. Is null
    # if no folder is open.
    #
    # @deprecated in favour of `rootUri`.
    root_path: Optional[str]

    # The rootUri of the workspace. Is null if no
    # folder is open. If both `rootPath` and `rootUri` are set
    # `rootUri` wins.
    #
    # @deprecated in favour of `workspaceFolders`
    root_uri: Optional[str]

    # User provided initialization options.
    initialization_options: Any

    # The capabilities provided by the client (editor or tool)
    capabilities: ClientCapabilities

    # The initial trace setting. If omitted trace is disabled ('off').
    trace: Optional[TraceValue]

    # The workspace folders configured in the client when the server starts.
    # This property is only available if the client supports workspace folders.
    # It can be `null` if the client supports workspace folders but none are
    # configured.
    #
    # @since 3.6.0
    workspace_folders: List[WorkspaceFolder]

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['process_id'] = source_dict.get('processId')

        client_info = source_dict.get('clientInfo')
        if client_info is not None and isinstance(client_info, dict):
            client_info = ClientServerInfo.from_dict(client_info)
        init_args['client_info'] = client_info

        init_args['locale'] = source_dict.get('locale')
        init_args['root_path'] = source_dict.get('rootPath')
        init_args['root_uri'] = source_dict.get('rootUri')
        init_args['initialization_options'] = source_dict.get('initializationOptions')

        init_args['capabilities'] = ClientCapabilities.from_dict(source_dict.get('capabilities'))

        trace_level = source_dict.get('trace')
        if trace_level is not None and isinstance(trace_level, str):
            trace_level = TraceValue(trace_level)
        init_args['trace'] = trace_level

        workspace_folders = source_dict.get('workspaceFolders')
        if workspace_folders is not None and isinstance(workspace_folders, list):
            workspace_folders = [
                WorkspaceFolder.from_dict(workspace_folder)
                for workspace_folder in workspace_folders
            ]
        init_args['workspace_folders'] = workspace_folders

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # We only need to parse the params
        raise NotImplementedError()


@dataclass
class InitializeResult(SerializableStructure):
    """
    Data structure which represents 'initialize' responses.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#initializeResult
    """
    # The capabilities the language server provides.
    capabilities: ServerCapabilities

    # Information about the server.
    server_info: Optional[ClientServerInfo]

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        raise NotImplementedError()

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create a result dictionary if we don't have one and set our fields
        result = result if result is not None else {}
        result['capabilities'] = self.capabilities.to_dict()
        if self.server_info is not None:
            result['serverInfo'] = self.server_info.to_dict()

        # Return the result.
        return result


@dataclass
class SetTraceParams(SerializableStructure):
    """
    Data structure which represents '$/setTrace' notification parameters.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#setTrace
    """
    # The new value that should be assigned to the trace setting.
    value: TraceValue

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['value'] = TraceValue(source_dict.get('value'))

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # We only need to parse the params
        raise NotImplementedError()


@dataclass
class ShowMessageParams(SerializableStructure):
    """
    Data structure which represents 'window/showMessage' requests.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#window_showMessage
    """
    # The message type.
    type: MessageType

    # The actual message.
    message: str

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        raise NotImplementedError()

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create a result dictionary if we don't have one and set our fields
        result = result if result is not None else {}
        result['type'] = int(self.type)
        result['message'] = self.message

        # Return the result.
        return result


@dataclass
class ShowDocumentParams(SerializableStructure):
    """
    Data structure which represents 'window/showDocument' requests.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#window_showDocument
    """
    # The document uri to show.
    uri: str

    # Indicates to show the resource in an external program.
    # To show for example `https://code.visualstudio.com/`
    # in the default WEB browser set `external` to `true`.
    external: Optional[bool]

    # An optional property to indicate whether the editor
    # showing the document should take focus or not.
    # Clients might ignore this property if an external
    # program is started.
    take_focus: Optional[bool]

    # An optional selection range if the document is a text
    # document. Clients might ignore the property if an
    # external program is started or the file is not a text
    # file.
    selection: Optional[Range]

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        raise NotImplementedError()

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create a result dictionary if we don't have one and set our fields
        result = result if result is not None else {}
        result['uri'] = self.uri
        if self.external is not None:
            result['external'] = self.external
        if self.take_focus is not None:
            result['takeFocus'] = self.take_focus
        if self.selection is not None:
            result['selection'] = self.selection.to_dict()

        # Return the result.
        return result


@dataclass
class ShowDocumentResult(SerializableStructure):
    """
    Data structure which represents 'window/showDocument' responses.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#window_showDocument
    """
    # A boolean indicating if the show was successful.
    success: bool

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['success'] = source_dict.get('success')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        raise NotImplementedError()


@dataclass
class LogMessageParams(SerializableStructure):
    """
    Data structure which represents 'window/logMessage' requests.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#window_logMessage
    """
    # The message type.
    type: MessageType

    # The actual message.
    message: str

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        raise NotImplementedError()

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create a result dictionary if we don't have one and set our fields
        result = result if result is not None else {}
        result['type'] = int(self.type)
        result['message'] = self.message

        # Return the result.
        return result


@dataclass
class WorkspaceFoldersChangeEvent(SerializableStructure):
    """
    Data structure which represents workspace folder change event data.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#workspaceFoldersChangeEvent
    """
    # The array of added workspace folders
    added: List[WorkspaceFolder]

    # The array of the removed workspace folder
    removed: List[WorkspaceFolder]

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        added_workspace_folders = source_dict.get('added')
        if added_workspace_folders is not None and isinstance(added_workspace_folders, list):
            added_workspace_folders = [
                WorkspaceFolder.from_dict(workspace_folder)
                for workspace_folder in added_workspace_folders
            ]
        init_args['added'] = added_workspace_folders

        removed_workspace_folders = source_dict.get('removed')
        if removed_workspace_folders is not None and isinstance(removed_workspace_folders, list):
            removed_workspace_folders = [
                WorkspaceFolder.from_dict(workspace_folder)
                for workspace_folder in removed_workspace_folders
            ]
        init_args['removed'] = removed_workspace_folders

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create a result dictionary if we don't have one and set our fields
        result = result if result is not None else {}
        if self.added is not None and isinstance(self.added, list):
            result['added'] = [folder.to_dict() for folder in self.added]
        if self.removed is not None and isinstance(self.removed, list):
            result['removed'] = [folder.to_dict() for folder in self.removed]

        # Return the result.
        return result


@dataclass
class DidChangeWorkspaceFoldersParams(SerializableStructure):
    """
    Data structure which represents 'workspace/didChangeWorkspaceFolders' notifications.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#didChangeWorkspaceFoldersParams
    """
    # The actual workspace folder change event.
    event: WorkspaceFoldersChangeEvent

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        event = source_dict.get('event')
        if event is not None:
            event = WorkspaceFoldersChangeEvent.from_dict(event)
        init_args['event'] = event

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        raise NotImplementedError()