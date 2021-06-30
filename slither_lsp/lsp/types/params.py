# pylint: disable=duplicate-code
from dataclasses import dataclass, field
from typing import Union, Any, Optional, List

from slither_lsp.lsp.types.capabilities import ClientCapabilities, ServerCapabilities
from slither_lsp.lsp.types.basic_structures import ClientServerInfo, TraceValue, WorkspaceFolder, MessageType, Range, \
    Diagnostic, TextDocumentIdentifier, Position
from slither_lsp.lsp.types.base_serializable_structure import SerializableStructure


@dataclass
class PartialResultParams(SerializableStructure):
    """
    Data structure which represents a parameter literal used to pass a partial result token.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#partialResultParams
    """
    # An optional token that a server can use to report partial results (e.g. streaming) to the client.
    partial_result_token: Union[str, int, None] = None


@dataclass
class WorkDoneProgressParams(SerializableStructure):
    """
    Data structure which represents a work done progress token.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#workDoneProgressParams
    """
    # An optional token that a server can use to report work done progress.
    work_done_token: Union[str, int, None] = None


@dataclass
class InitializeParams(WorkDoneProgressParams):
    """
    Data structure which represents 'initialize' request parameters.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#initializeParams
    """
    # The process Id of the parent process that started the server. Is null if
    # the process has not been started by another process. If the parent
    # process is not alive then the server should exit (see exit notification)
    # its process.
    process_id: Optional[int] = None

    # Information about the client
    client_info: Optional[ClientServerInfo] = None

    # The locale the client is currently showing the user interface
    # in. This must not necessarily be the locale of the operating
    # system.
    #
    # Uses IETF language tags as the value's syntax
    # (See https://en.wikipedia.org/wiki/IETF_language_tag)
    # @since 3.16.0
    locale: Optional[str] = None

    # The rootPath of the workspace. Is null
    # if no folder is open.
    #
    # @deprecated in favour of `rootUri`.
    root_path: Optional[str] = None

    # The rootUri of the workspace. Is null if no
    # folder is open. If both `rootPath` and `rootUri` are set
    # `rootUri` wins.
    #
    # @deprecated in favour of `workspaceFolders`
    root_uri: Optional[str] = None

    # User provided initialization options.
    initialization_options: Any = None

    # The capabilities provided by the client (editor or tool)
    capabilities: ClientCapabilities = field(default_factory=ClientCapabilities)

    # The initial trace setting. If omitted trace is disabled ('off').
    trace: Optional[TraceValue] = None

    # The workspace folders configured in the client when the server starts.
    # This property is only available if the client supports workspace folders.
    # It can be `null` if the client supports workspace folders but none are
    # configured.
    # @since 3.6.0
    workspace_folders: List[WorkspaceFolder] = field(default_factory=list)


@dataclass
class InitializeResult(SerializableStructure):
    """
    Data structure which represents 'initialize' responses.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#initializeResult
    """
    # The capabilities the language server provides.
    capabilities: ServerCapabilities = field(default_factory=ServerCapabilities)

    # Information about the server.
    server_info: Optional[ClientServerInfo] = None


@dataclass
class SetTraceParams(SerializableStructure):
    """
    Data structure which represents '$/setTrace' notification parameters.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#setTrace
    """
    # The new value that should be assigned to the trace setting.
    value: TraceValue = TraceValue.OFF


@dataclass
class ShowMessageParams(SerializableStructure):
    """
    Data structure which represents 'window/showMessage' requests.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#window_showMessage
    """
    # The message type.
    type: MessageType = MessageType.LOG

    # The actual message.
    message: str = ""


@dataclass
class ShowDocumentParams(SerializableStructure):
    """
    Data structure which represents 'window/showDocument' requests.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#window_showDocument
    """
    # The document uri to show.
    uri: str = ""

    # Indicates to show the resource in an external program.
    # To show for example `https://code.visualstudio.com/`
    # in the default WEB browser set `external` to `true`.
    external: Optional[bool] = None

    # An optional property to indicate whether the editor
    # showing the document should take focus or not.
    # Clients might ignore this property if an external
    # program is started.
    take_focus: Optional[bool] = None

    # An optional selection range if the document is a text
    # document. Clients might ignore the property if an
    # external program is started or the file is not a text
    # file.
    selection: Optional[Range] = None


@dataclass
class ShowDocumentResult(SerializableStructure):
    """
    Data structure which represents 'window/showDocument' responses.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#window_showDocument
    """
    # A boolean indicating if the show was successful.
    success: bool = False


@dataclass
class LogMessageParams(SerializableStructure):
    """
    Data structure which represents 'window/logMessage' requests.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#window_logMessage
    """
    # The message type.
    type: MessageType = MessageType.LOG

    # The actual message.
    message: str = ""


@dataclass
class WorkspaceFoldersChangeEvent(SerializableStructure):
    """
    Data structure which represents workspace folder change event data.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#workspaceFoldersChangeEvent
    """
    # The array of added workspace folders
    added: List[WorkspaceFolder] = field(default_factory=list)

    # The array of the removed workspace folder
    removed: List[WorkspaceFolder] = field(default_factory=list)


@dataclass
class DidChangeWorkspaceFoldersParams(SerializableStructure):
    """
    Data structure which represents 'workspace/didChangeWorkspaceFolders' notifications.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#didChangeWorkspaceFoldersParams
    """
    # The actual workspace folder change event.
    event: WorkspaceFoldersChangeEvent = field(default_factory=WorkspaceFoldersChangeEvent)


@dataclass
class PublishDiagnosticsParams(SerializableStructure):

    """
    Data structure which represents 'textDocument/publishDiagnostics' notifications.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#publishDiagnosticsParams
    """
    uri: str = ""
    version: Optional[int] = None
    diagnostics: List[Diagnostic] = field(default_factory=list)


@dataclass
class TextDocumentPositionParams(SerializableStructure):
    """
    Data structure which represents 'initialize' request parameters.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocumentPositionParams
    """
    # The text document
    text_document: TextDocumentIdentifier = field(default_factory=TextDocumentIdentifier)

    # The position inside the text document.
    position: Position = field(default_factory=Position)


@dataclass
class DeclarationParams(TextDocumentPositionParams, WorkDoneProgressParams, PartialResultParams):
    """
    Data structure which represents 'textDocument/declaration' request parameters.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#declarationParams
    """
    # Note: For now this just inherits from its base classes.
    pass


@dataclass
class DefinitionParams(TextDocumentPositionParams, WorkDoneProgressParams, PartialResultParams):
    """
    Data structure which represents 'textDocument/definition' request parameters.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#definitionParams
    """
    # Note: For now this just inherits from its base classes.
    pass


@dataclass
class TypeDefinitionParams(TextDocumentPositionParams, WorkDoneProgressParams, PartialResultParams):
    """
    Data structure which represents 'textDocument/typeDefinition' request parameters.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#typeDefinitionParams
    """
    # Note: For now this just inherits from its base classes.
    pass


@dataclass
class ImplementationParams(TextDocumentPositionParams, WorkDoneProgressParams, PartialResultParams):
    """
    Data structure which represents 'textDocument/implementation' request parameters.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#implementationParams
    """
    # Note: For now this just inherits from its base classes.
    pass


@dataclass
class ReferenceContext(SerializableStructure):
    """
    Data structure which represents 'textDocument/references' request parameters.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#referenceContext
    """
    # Include the declaration of the current symbol.
    include_declaration: bool = False


@dataclass
class ReferenceParams(TextDocumentPositionParams, WorkDoneProgressParams, PartialResultParams):
    """
    Data structure which represents 'textDocument/references' request parameters.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#referenceParams
    """
    context: ReferenceContext = field(default_factory=ReferenceContext)


@dataclass
class DocumentHighlightParams(TextDocumentPositionParams, WorkDoneProgressParams, PartialResultParams):
    """
    Data structure which represents 'textDocument/documentHighlight' request parameters.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#documentHighlightParams
    """
    # Note: For now this just inherits from its base classes.
    pass


@dataclass
class MonikerParams(TextDocumentPositionParams, WorkDoneProgressParams, PartialResultParams):
    """
    Data structure which represents 'textDocument/moniker' request parameters.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#monikerParams
    """
    # Note: For now this just inherits from its base classes.
    pass
