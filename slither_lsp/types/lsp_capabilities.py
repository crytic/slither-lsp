from dataclasses import dataclass, field
from typing import Any, Optional, Union, List

from slither_lsp.types.base_serializable_structure import SerializableStructure
from slither_lsp.types.lsp_basic_structures import DiagnosticTag


# region Server Capabilities


@dataclass
class WorkDoneProgressOptions(SerializableStructure):
    """
    Data structure which represents capabilities to see if work done progress can be tracked.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#workDoneProgressOptions
    """

    work_done_progress: Optional[bool] = None


@dataclass
class DeclarationOptions(WorkDoneProgressOptions):
    """
    Data structure which represents declaration options provided via capabilities.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#declarationOptions
    """
    # NOTE: This simply inherits from WorkDoneProgressOptions for now
    pass


@dataclass
class DefinitionOptions(WorkDoneProgressOptions):
    """
    Data structure which represents definition options provided via capabilities.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#definitionOptions
    """
    # NOTE: This simply inherits from WorkDoneProgressOptions for now
    pass


@dataclass
class TypeDefinitionOptions(WorkDoneProgressOptions):
    """
    Data structure which represents type definition options provided via capabilities.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#typeDefinitionOptions
    """
    # NOTE: This simply inherits from WorkDoneProgressOptions for now
    pass


@dataclass
class ImplementationOptions(WorkDoneProgressOptions):
    """
    Data structure which represents implementation options provided via capabilities.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#implementationOptions
    """
    # NOTE: This simply inherits from WorkDoneProgressOptions for now
    pass


@dataclass
class ReferenceOptions(WorkDoneProgressOptions):
    """
    Data structure which represents find reference options provided via capabilities.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#referenceOptions
    """
    # NOTE: This simply inherits from WorkDoneProgressOptions for now
    pass


@dataclass
class DocumentHighlightOptions(WorkDoneProgressOptions):
    """
    Data structure which represents document highlight options provided via capabilities.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#documentHighlightOptions
    """
    # NOTE: This simply inherits from WorkDoneProgressOptions for now
    pass


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


@dataclass
class WorkspaceServerCapabilities(SerializableStructure):
    """
    Data structure which represents workspace specific server capabilities.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#serverCapabilities
    """
    workspace_folders: Optional[WorkspaceFoldersServerCapabilities] = field(
        default_factory=WorkspaceFoldersServerCapabilities
    )


@dataclass
class ServerCapabilities(SerializableStructure):
    """
    Data structure which represents capabilities a server supports.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#serverCapabilities
    """

    # The server provides go to declaration support.
    # @since 3.14.0
    # TODO: Once we add DeclarationRegistrationOptions, we need to add logic for it here, as it should be another
    #  possible value type for this field.
    declaration_provider: Union[bool, DeclarationOptions, None] = None

    # The server provides goto definition support.
    definition_provider: Union[bool, DefinitionOptions, None] = None

    # The server provides goto type definition support.
    # @since 3.6.0
    # TODO: Once we add TypeDefinitionRegistrationOptions, we need to add logic for it here, as it should be another
    #  possible value type for this field.
    type_definition_provider: Union[bool, TypeDefinitionOptions, None] = None

    # The server provides goto implementation support.
    # @since 3.6.0
    # TODO: Once we add ImplementationRegistrationOptions, we need to add logic for it here, as it should be another
    #  possible value type for this field.
    implementation_provider: Union[bool, ImplementationOptions, None] = None

    # The server provides find references support.
    references_provider: Union[bool, ReferenceOptions, None] = None

    # The server provides document highlight support.
    document_highlight_provider: Union[bool, DocumentHighlightOptions, None] = None

    # Workspace specific server capabilities
    workspace: Optional[WorkspaceServerCapabilities] = field(default_factory=WorkspaceServerCapabilities)

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
    # @since 3.15.0
    work_done_progress: Optional[bool] = None

    # TODO: showMessage

    # Client capabilities for the show document request.
    # @since 3.16.0
    show_document: Optional[ShowDocumentClientCapabilities] = None


@dataclass
class PublishDiagnosticsTagSupportClientCapabilities(SerializableStructure):
    """
     Data structure which contains tag support information ('tagSupport' in 'PublishDiagnosticsClientCapabilities')
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#publishDiagnosticsClientCapabilities
    """
    # Whether the clients accepts diagnostics with related information.
    value_set: List[DiagnosticTag] = field(default_factory=list)


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
    # @since 3.15.0
    tag_support: Optional[PublishDiagnosticsTagSupportClientCapabilities] = None

    # Whether the client interprets the version property of the
    # `textDocument/publishDiagnostics` notification's parameter.
    # @since 3.15.0
    version_support: Optional[bool] = None

    # Client supports a codeDescription property
    # @since 3.16.0
    code_description_support: Optional[bool] = None

    # Whether code action supports the `data` property which is
    # preserved between a `textDocument/publishDiagnostics` and
    # `textDocument/codeAction` request.
    # @since 3.16.0
    data_support: Optional[bool] = None


@dataclass
class DeclarationClientCapabilities(SerializableStructure):
    """
     Data structure which contains capabilities specific to the 'textDocument/declaration' request.
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocumentClientCapabilities
    """
    # Whether declaration supports dynamic registration. If this is set to
    # `true` the client supports the new `DeclarationRegistrationOptions`
    # return value for the corresponding server capability as well.
    dynamic_registration: Optional[bool] = None

    # The client supports additional metadata in the form of declaration links.
    link_support: Optional[bool] = None


@dataclass
class DefinitionClientCapabilities(SerializableStructure):
    """
     Data structure which contains capabilities specific to the 'textDocument/definition' request.
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#definitionClientCapabilities
    """
    # Whether definition supports dynamic registration.
    dynamic_registration: Optional[bool] = None

    # The client supports additional metadata in the form of definition links.
    # @since 3.14.0
    link_support: Optional[bool] = None


@dataclass
class TypeDefinitionClientCapabilities(SerializableStructure):
    """
     Data structure which contains capabilities specific to the 'textDocument/typeDefinition' request.
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#typeDefinitionClientCapabilities
    """
    # Whether implementation supports dynamic registration. If this is set to
    # `true` the client supports the new `TypeDefinitionRegistrationOptions`
    # return value for the corresponding server capability as well.
    dynamic_registration: Optional[bool] = None

    # The client supports additional metadata in the form of definition links.
    # @since 3.14.0
    link_support: Optional[bool] = None


@dataclass
class ImplementationClientCapabilities(SerializableStructure):
    """
     Data structure which contains capabilities specific to the 'textDocument/implementation' request.
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#implementationClientCapabilities
    """
    # Whether implementation supports dynamic registration. If this is set to
    # `true` the client supports the new `ImplementationRegistrationOptions`
    # return value for the corresponding server capability as well.
    dynamic_registration: Optional[bool] = None

    # The client supports additional metadata in the form of definition links.
    # @since 3.14.0
    link_support: Optional[bool] = None


@dataclass
class ReferenceClientCapabilities(SerializableStructure):
    """
     Data structure which contains capabilities specific to the 'textDocument/references' request.
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#referenceClientCapabilities
    """
    # Whether references supports dynamic registration.
    dynamic_registration: Optional[bool] = None


@dataclass
class DocumentHighlightClientCapabilities(SerializableStructure):
    """
     Data structure which contains capabilities specific to the 'textDocument/documentHighlight' request.
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocument_documentHighlight
    """
    # Whether document highlight supports dynamic registration.
    dynamic_registration: Optional[bool] = None


@dataclass
class TextDocumentClientCapabilities(SerializableStructure):
    """
     Data structure which represents text document specific client capabilities.
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocumentClientCapabilities
    """
    # Capabilities specific to the `textDocument/declaration` request.
    # @since 3.14.0
    declaration: Optional[DeclarationClientCapabilities] = None

    # Capabilities specific to the `textDocument/definition` request.
    definition: Optional[DefinitionClientCapabilities] = None

    # Capabilities specific to the `textDocument/typeDefinition` request.
    # @since 3.6.0
    type_definition: Optional[TypeDefinitionClientCapabilities] = None

    # Capabilities specific to the `textDocument/implementation` request.
    # @since 3.6.0
    implementation: Optional[ImplementationClientCapabilities] = None

    # Capabilities specific to the `textDocument/references` request.
    references: Optional[ReferenceClientCapabilities] = None

    # Capabilities specific to the `textDocument/publishDiagnostics` notification.
    publish_diagnostics: Optional[PublishDiagnosticsClientCapabilities] = None

    # Capabilities specific to the `textDocument/documentHighlight` request.
    document_highlight: Optional[DocumentHighlightClientCapabilities] = None


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
    # @since 3.6.0
    workspace_folders: Optional[bool] = None

    # The client supports `workspace/configuration` requests.
    # @since 3.6.0
    configuration: Optional[bool] = None

    # TODO: semanticTokens, codeLens, fileOperations, textDocument, window, general,

    # Experimental client capabilities.
    experimental: Any = None


@dataclass
class ClientCapabilities(SerializableStructure):
    """
    Data structure which represents capabilities a client supports.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#clientCapabilities
    """
    # Workspace specific client capabilities.
    workspace: Optional[WorkspaceClientCapabilities] = field(default_factory=WorkspaceClientCapabilities)

    # Window specific client capabilities.
    window: Optional[WindowClientCapabilities] = field(default_factory=WindowClientCapabilities)

    # Text document specific client capabilities.
    text_document: Optional[TextDocumentClientCapabilities] = field(default_factory=TextDocumentClientCapabilities)

# endregion
