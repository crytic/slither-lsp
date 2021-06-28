from dataclasses import dataclass, field
from typing import Any, Optional, Union, List

from slither_lsp.types.base_serializable_structure import SerializableStructure


# region Server Capabilities
from slither_lsp.types.lsp_basic_structures import DiagnosticTag


@dataclass
class WorkspaceFoldersServerCapabilities(SerializableStructure):
    """
    Data structure which represents workspace folder specific server capabilities.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#workspaceFoldersServerCapabilities
    """
    # The server has support for workspace folders
    supported: Optional[bool] = None

    # Whether the server wants to receive workspace folder
    # change notifications.
    #
    # If a string is provided, the string is treated as an ID
    # under which the notification is registered on the client
    # side. The ID can be used to unregister for these events
    # using the `client/unregisterCapability` request.
    change_notifications: Union[str, bool, None] = None

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['supported'] = source_dict.get('supported')
        init_args['change_notifications'] = source_dict.get('changeNotifications')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}
        if self.supported is not None:
            result['supported'] = self.supported
        if self.change_notifications is not None:
            result['changeNotifications'] = self.change_notifications
        return result


@dataclass
class WorkspaceServerCapabilities(SerializableStructure):
    """
    Data structure which represents workspace specific server capabilities.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#serverCapabilities
    """
    workspace_folders: Optional[WorkspaceFoldersServerCapabilities] = WorkspaceFoldersServerCapabilities()

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        workspace_folders = source_dict.get('workspaceFolders')
        if workspace_folders is not None:
            workspace_folders = WorkspaceFoldersServerCapabilities.from_dict(workspace_folders)
        init_args['workspace_folders'] = workspace_folders

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}

        if self.workspace_folders is not None:
            result['workspaceFolders'] = self.workspace_folders.to_dict()

        return result


@dataclass
class ServerCapabilities(SerializableStructure):
    """
    Data structure which represents capabilities a server supports.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#serverCapabilities
    """
    workspace: Optional[WorkspaceServerCapabilities] = WorkspaceServerCapabilities()

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        workspace = source_dict.get('workspace')
        if workspace is not None:
            workspace = WorkspaceServerCapabilities.from_dict(workspace)
        init_args['workspace'] = workspace

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}
        if self.workspace is not None:
            result['workspace'] = self.workspace.to_dict()
        return result

# endregion


# region Client Capabilities

@dataclass
class ShowDocumentClientCapabilities(SerializableStructure):
    """
    Data structure which represents capabilities for the request to display a document.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#window_showDocument
    """
    # The client has support for the show document request.
    support: bool = False

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['support'] = source_dict.get('support')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}
        result['support'] = self.support
        return result


@dataclass
class WindowClientCapabilities(SerializableStructure):
    """
     Data structure which represents window specific client capabilities.
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#clientCapabilities
    """
    # Whether client supports handling progress notifications. If set
    # servers are allowed to report in `workDoneProgress` property in the
    # request specific server capabilities.
    #
    # @since 3.15.0
    work_done_progress: Optional[bool] = None

    # TODO: showMessage

    # Client capabilities for the show document request.
    #
    # @since 3.16.0
    show_document: Optional[ShowDocumentClientCapabilities] = None

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['work_done_progress'] = source_dict.get('workDoneProgress')
        show_document = source_dict.get('showDocument')
        if show_document is not None:
            show_document = ShowDocumentClientCapabilities.from_dict(show_document)
        init_args['show_document'] = show_document

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}

        if self.work_done_progress is not None:
            result['workDoneProgress'] = self.work_done_progress
        if self.show_document is not None:
            result['showDocument'] = self.show_document.to_dict()

        return result


@dataclass
class PublishDiagnosticsTagSupportClientCapabilities(SerializableStructure):
    """
     Data structure which contains tag support information ('tagSupport' in 'PublishDiagnosticsClientCapabilities')
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#publishDiagnosticsClientCapabilities
    """
    # Whether the clients accepts diagnostics with related information.
    value_set: List[DiagnosticTag] = field(default_factory=list)

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        value_set: List[int] = source_dict.get('valueSet')
        if value_set is not None:
            value_set = [DiagnosticTag(v) for v in value_set]
        init_args['value_set'] = value_set

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}

        if self.value_set is not None:
            result['valueSet'] = self.value_set

        return result


@dataclass
class PublishDiagnosticsClientCapabilities(SerializableStructure):
    """
     Data structure which represents text document specific client capabilities.
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#publishDiagnosticsClientCapabilities
    """
    # Whether the clients accepts diagnostics with related information.
    related_information: Optional[bool] = None

    # Client supports the tag property to provide meta data about a diagnostic.
    # Clients supporting tags have to handle unknown tags gracefully.
    #
    # @since 3.15.0
    tag_support: Optional[PublishDiagnosticsTagSupportClientCapabilities] = \
        PublishDiagnosticsTagSupportClientCapabilities()

    # Whether the client interprets the version property of the
    # `textDocument/publishDiagnostics` notification's parameter.
    #
    # @since 3.15.0
    version_support: Optional[bool] = None

    # Client supports a codeDescription property
    #
    # @since 3.16.0
    code_description_support: Optional[bool] = None

    # Whether code action supports the `data` property which is
    # preserved between a `textDocument/publishDiagnostics` and
    # `textDocument/codeAction` request.
    #
    # @since 3.16.0
    data_support: Optional[bool] = None

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['related_information'] = source_dict.get('relatedInformation')

        tag_support = source_dict.get('tagSupport')
        if tag_support is not None:
            tag_support = PublishDiagnosticsTagSupportClientCapabilities.from_dict(tag_support)
        init_args['tag_support'] = tag_support

        init_args['version_support'] = source_dict.get('versionSupport')
        init_args['code_description_support'] = source_dict.get('codeDescriptionSupport')
        init_args['data_support'] = source_dict.get('dataSupport')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}

        if self.related_information is not None:
            result['relatedInformation'] = self.related_information
        if self.tag_support is not None:
            result['tagSupport'] = self.tag_support.to_dict()
        if self.version_support is not None:
            result['versionSupport'] = self.version_support
        if self.code_description_support is not None:
            result['codeDescriptionSupport'] = self.code_description_support
        if self.data_support is not None:
            result['dataSupport'] = self.data_support

        return result


@dataclass
class TextDocumentClientCapabilities(SerializableStructure):
    """
     Data structure which represents text document specific client capabilities.
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocumentClientCapabilities
    """
    # Capabilities specific to the `textDocument/publishDiagnostics` notification.
    publish_diagnostics: Optional[PublishDiagnosticsClientCapabilities] = PublishDiagnosticsClientCapabilities()

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        publish_diagnostics = source_dict.get('publishDiagnostics')
        if publish_diagnostics is not None:
            publish_diagnostics = PublishDiagnosticsClientCapabilities.from_dict(publish_diagnostics)
        init_args['publish_diagnostics'] = publish_diagnostics

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}

        if self.publish_diagnostics is not None:
            result['publishDiagnostics'] = self.publish_diagnostics.to_dict()

        return result


@dataclass
class WorkspaceClientCapabilities(SerializableStructure):
    """
     Data structure which represents workspace specific client capabilities.
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#clientCapabilities
     """
    # The client supports applying batch edits
    # to the workspace by supporting the request
    # 'workspace/applyEdit'
    apply_edit: Optional[bool] = None

    # TODO: workspaceEdit, didChangeConfiguration, didChangeWatchedFiles, symbol, executeCommand

    # The client has support for workspace folders.
    #
    # @since 3.6.0
    workspace_folders: Optional[bool] = None

    # The client supports `workspace/configuration` requests.
    #
    # @since 3.6.0
    configuration: Optional[bool] = None

    # TODO: semanticTokens, codeLens, fileOperations, textDocument, window, general,

    # Experimental client capabilities.
    experimental: Any = None

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['apply_edit'] = source_dict.get('applyEdit')
        init_args['workspace_folders'] = source_dict.get('workspaceFolders')
        init_args['configuration'] = source_dict.get('configuration')
        init_args['experimental'] = source_dict.get('experimental')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}

        if self.apply_edit is not None:
            result['applyEdit'] = self.apply_edit
        if self.workspace_folders is not None:
            result['workspaceFolders'] = self.workspace_folders
        if self.configuration is not None:
            result['configuration'] = self.configuration
        if self.experimental is not None:
            result['experimental'] = self.experimental

        return result


@dataclass
class ClientCapabilities(SerializableStructure):
    """
    Data structure which represents capabilities a client supports.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#clientCapabilities
    """
    # Workspace specific client capabilities.
    workspace: Optional[WorkspaceClientCapabilities] = WorkspaceClientCapabilities()

    # Window specific client capabilities.
    window: Optional[WindowClientCapabilities] = WindowClientCapabilities()

    # Text document specific client capabilities.
    text_document: Optional[TextDocumentClientCapabilities] = TextDocumentClientCapabilities()

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        workspace = source_dict.get('workspace')
        if workspace is not None:
            workspace = WorkspaceClientCapabilities.from_dict(workspace)
        init_args['workspace'] = workspace

        window = source_dict.get('window')
        if window is not None:
            window = WindowClientCapabilities.from_dict(window)
        init_args['window'] = window

        text_document = source_dict.get('textDocument')
        if text_document is not None:
            text_document = TextDocumentClientCapabilities.from_dict(text_document)
        init_args['text_document'] = text_document

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}

        if self.workspace is not None:
            result['workspace'] = self.workspace.to_dict()
        if self.window is not None:
            result['window'] = self.window.to_dict()
        if self.text_document is not None:
            result['textDocument'] = self.text_document.to_dict()

        return result

# endregion
