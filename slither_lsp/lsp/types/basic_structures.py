from dataclasses import dataclass, field
from enum import IntEnum, Enum
from typing import Optional, Any, Union, List, Dict

# These structures ideally would just be dataclass objects, so we could cast dictionaries to dataclasses.
# However, dataclasses cannot initialize with unexpected parameters, and we can't assume the Language Server
# Protocol won't change and add more keys. So we add our own serializing/deserializing methods on top of
# this while still reaping benefits of auto-constructor generation, parameter validation, etc from dataclass.
# See more at the link below:
# https://microsoft.github.io/language-server-protocol/specifications/specification-current/#basic-json-structures

# Text documents have a defined EOL.
# https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocuments
from slither_lsp.lsp.types.base_serializable_structure import SerializableStructure, serialization_metadata

EOL = ['\n', '\r\n', '\r']


@dataclass
class ClientServerInfo(SerializableStructure):
    """
    Data structure which describes a client/server by name and version.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#initialize
    """

    # The name of the client/server as defined by itself.
    name: str

    # The client/server's version as defined by itself.
    version: Optional[str] = None


class MessageType(IntEnum):
    """
    Defines the severity level of a message to be shown/logged.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#messageType
    """
    ERROR = 1
    WARNING = 2
    INFO = 3
    LOG = 4


@dataclass
class WorkspaceFolder(SerializableStructure):
    """
    Data structure which describes a workspace folder by name and location (uri).
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#workspaceFolder
    """
    # The associated URI for this workspace folder.
    uri: str

    # The name of the workspace folder. Used to refer to this
    # workspace folder in the user interface.
    name: Optional[str] = None


@dataclass
class Position(SerializableStructure):
    """
    Data structure which represents a position within a text file by line number and character index (column).
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#position
    """
    # Line position in a document (zero-based).
    line: int

    # Character offset on a line in a document (zero-based). Assuming that
    # the line is represented as a string, the `character` value represents
    # the gap between the `character` and `character + 1`.
    #
    # If the character value is greater than the line length it defaults back
    # to the line length.
    character: int


@dataclass
class Range(SerializableStructure):
    """
    Data structure which represents a position range in a text file.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#range
    """
    # The range's start position.
    start: Position

    # The range's end position.
    end: Position


@dataclass
class Location(SerializableStructure):
    """
    Data structure which represents a text file location (file uri and position range).
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#location
    """
    uri: str
    range: Range


@dataclass
class LocationLink(SerializableStructure):
    """
    Data structure which represents a link between a source and target destination.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#locationLink
    """
    # The target resource identifier of this link.
    target_uri: str

    # The full target range of this link. If the target for example is a symbol
    # then target range is the range enclosing this symbol not including
    # leading/trailing whitespace but everything else like comments. This
    # information is typically used to highlight the range in the editor.
    target_range: Range

    # The range that should be selected and revealed when this link is being
    # followed, e.g the name of a function. Must be contained by the the
    # `targetRange`. See also `DocumentSymbol#range`
    target_selection_range: Range

    # Span of the origin of the link.
    # Used as the underlined span for mouse interaction. Defaults to the word
    # range at the mouse position.
    origin_selection_range: Optional[Range] = None


class DiagnosticSeverity(IntEnum):
    """
    Defines the severity level of a diagnostic (compiler error, warning, etc).
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#diagnosticSeverity
    """
    ERROR = 1
    WARNING = 2
    INFORMATION = 3
    HINT = 4


class DiagnosticTag(IntEnum):
    """
    Diagnostic tags describe code. Tags include 'unnecessary', 'deprecated', etc.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#diagnosticTag
    """
    # Unused or unnecessary code.
    #
    # Clients are allowed to render diagnostics with this tag faded out
    # instead of having an error squiggle.
    UNNECESSARY = 1

    # Deprecated or obsolete code.
    #
    # Clients are allowed to rendered diagnostics with this tag strike through.
    DEPRECATED = 2


@dataclass
class DiagnosticRelatedInformation(SerializableStructure):
    """
    Data structure which represents a related message and source code location for a diagnostic.
    This should be used to point to code locations that cause or are related to a diagnostic, e.g when duplicating a
    symbol in scope.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#diagnosticRelatedInformation
    """
    location: Location
    message: str


@dataclass
class CodeDescription(SerializableStructure):
    """
    Data structure which represents a description for an error code.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#codeDescription
    """
    href: str


@dataclass
class Diagnostic(SerializableStructure):
    """
    Data structure which represents a diagnostic (compiler error, warning, etc). Diagnostic objects are only valid
    in the scope of a resource.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#diagnostic
    """
    # The range at which the message applies.
    range: Range

    # The diagnostic's message.
    message: str

    # The diagnostic's severity. Can be omitted. If omitted it is up to the
    # client to interpret diagnostics as error, warning, info or hint.
    severity: Optional[DiagnosticSeverity] = None

    # The diagnostic's code, which might appear in the user interface.
    code: Union[int, str, None] = None

    # An optional property to describe the error code.
    code_description: Optional[CodeDescription] = None

    # A human-readable string describing the source of this
    # diagnostic, e.g. 'typescript' or 'super lint'.
    source: Optional[str] = None

    # Additional metadata about the diagnostic.
    tags: Optional[List[DiagnosticTag]] = None

    # An array of related diagnostic information, e.g. when symbol-names within
    # a scope collide all definitions can be marked via this property.
    related_information: Optional[List[DiagnosticRelatedInformation]] = None

    # A data entry field that is preserved between a
    # `textDocument/publishDiagnostics` notification and
    # `textDocument/codeAction` request.
    data: Any = None


@dataclass
class Command(SerializableStructure):
    """
    Data structure which represents a command which can be registered on the client side to be invoked on the server.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-current/#command
    """
    # The title of the command, like `save`.
    title: str

    # The identifier of the actual command handler
    command: str

    # Arguments that the command handler should be invoked with
    arguments: Optional[List[Any]] = None


@dataclass
class TextEdit(SerializableStructure):
    """
    Data structure which represents a textual edit applicable to a text document.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textEdit
    """
    # The range of the text document to be manipulated. To insert
    # text into a document create a range where start === end.
    range: Range

    # The string to be inserted. For delete operations use an
    # empty string.
    new_text: str


@dataclass
class ChangeAnnotation(SerializableStructure):
    """
    Data structure which represents additional information regarding document changes.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#changeAnnotation
    """
    # A human-readable string describing the actual change. The string
    # is rendered prominent in the user interface.
    label: str

    # A flag which indicates that user confirmation is needed
    # before applying the change.
    needs_confirmation: Optional[bool] = None

    # A human-readable string which is rendered less prominent in
    # the user interface.
    description: Optional[str] = None


@dataclass
class AnnotatedTextEdit(TextEdit):
    """
    Data structure which represents a special text edit with an additional change annotation.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#annotatedTextEdit
    """
    # The actual annotation identifier.
    annotation_id: str


@dataclass
class TextDocumentIdentifier(SerializableStructure):
    """
    Data structure which represents a text document identifier (uri).
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocumentIdentifier
    """
    # The actual annotation identifier.
    uri: str


@dataclass
class VersionedTextDocumentIdentifier(TextDocumentIdentifier):
    """
    Data structure which represents an identifier to denote a specific version of a text document.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#versionedTextDocumentIdentifier
    """

    # The version number of this document. If an optional versioned text document
    # identifier is sent from the server to the client and the file is not
    # open in the editor (the server has not received an open notification
    # before) the server can send `null` to indicate that the version is
    # known and the content on disk is the master (as specified with document
    # content ownership).
    #
    # The version number of a document will increase after each change,
    # including undo/redo. The number doesn't need to be consecutive.
    version: Optional[int] = field(default=None, metadata=serialization_metadata(include_none=True))  # int | null


@dataclass
class OptionalVersionedTextDocumentIdentifier(TextDocumentIdentifier):
    """
    Data structure which represents an identifier which optionally denotes a specific version of a text document.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#optionalVersionedTextDocumentIdentifier
    """

    # The version number of this document. If an optional versioned text document
    # identifier is sent from the server to the client and the file is not
    # open in the editor (the server has not received an open notification
    # before) the server can send `null` to indicate that the version is
    # known and the content on disk is the master (as specified with document
    # content ownership).
    #
    # The version number of a document will increase after each change,
    # including undo/redo. The number doesn't need to be consecutive.
    version: Optional[int] = field(default=None, metadata=serialization_metadata(include_none=True))  # int | null


@dataclass
class TextDocumentEdit(SerializableStructure):
    """
    Data structure which represents describes textual changes on a single text document.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocumentEdit
    """

    # The text document to change.
    text_document: OptionalVersionedTextDocumentIdentifier

    # The edits to be applied.
    # @since 3.16.0 - support for AnnotatedTextEdit. This is guarded by the
    # client capability `workspace.workspaceEdit.changeAnnotationSupport`
    edits: List[Union[AnnotatedTextEdit, TextEdit]]


@dataclass
class CreateFileOptions(SerializableStructure):
    """
    Data structure which represents options to create a file.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#createFileOptions
    """
    # Overwrite existing file. Overwrite wins over `ignoreIfExists`
    overwrite: Optional[bool]

    # Ignore if exists.
    ignore_if_exists: Optional[bool]


@dataclass
class CreateFile(SerializableStructure):
    """
    Data structure which represents a create file operation.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#createFile
    """
    # The resource to create.
    uri: str

    # Additional options
    options: Optional[CreateFileOptions]

    # An optional annotation identifier describing the operation.
    # @since 3.16.0
    annotation_id: Optional[str]

    # A create
    kind: str = field(default='create', metadata=serialization_metadata(enforce_as_constant=True))


@dataclass
class RenameFileOptions(SerializableStructure):
    """
    Data structure which represents options to rename a file.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#renameFileOptions
    """
    # Overwrite target if existing. Overwrite wins over `ignoreIfExists`
    overwrite: Optional[bool]

    # Ignore if target exists.
    ignore_if_exists: Optional[bool]


@dataclass
class RenameFile(SerializableStructure):
    """
    Data structure which represents a rename file operation.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#renameFile
    """
    # The old (existing) location.
    old_uri: str

    # The new location.
    new_uri: str

    # Rename options
    options: Optional[RenameFileOptions]

    # An optional annotation identifier describing the operation.
    # @since 3.16.0
    annotation_id: Optional[str]

    # A rename
    kind: str = field(default='rename', metadata=serialization_metadata(enforce_as_constant=True))


@dataclass
class DeleteFileOptions(SerializableStructure):
    """
    Data structure which represents options to delete a file.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#deleteFileOptions
    """
    # Delete the content recursively if a folder is denoted.
    recursive: Optional[bool]

    # Ignore if target exists.
    ignore_if_exists: Optional[bool]


@dataclass
class DeleteFile(SerializableStructure):
    """
    Data structure which represents a delete file operation.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#deleteFile
    """
    # The file to delete.
    uri: str

    # Delete options.
    options: Optional[DeleteFileOptions]

    # An optional annotation identifier describing the operation.
    # @since 3.16.0
    annotation_id: Optional[str]

    # A delete
    kind: str = field(default='delete', metadata=serialization_metadata(enforce_as_constant=True))


@dataclass
class WorkspaceEdit(SerializableStructure):
    """
    Data structure which represents changes to many resources managed in the workspace.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#workspaceEdit
    """
    # Holds changes to existing resources.
    changes: Optional[Dict[str, List[TextEdit]]]

    # Depending on the client capability
    # `workspace.workspaceEdit.resourceOperations` document changes are either
    # an array of `TextDocumentEdit`s to express changes to n different text
    # documents where each text document edit addresses a specific version of
    # a text document. Or it can contain above `TextDocumentEdit`s mixed with
    # create, rename and delete file / folder operations.
    #
    # Whether a client supports versioned document edits is expressed via
    # `workspace.workspaceEdit.documentChanges` client capability.
    #
    # If a client neither supports `documentChanges` nor
    # `workspace.workspaceEdit.resourceOperations` then only plain `TextEdit`s
    # using the `changes` property are supported.
    document_changes: Union[List[TextDocumentEdit], List[Union[TextDocumentEdit, CreateFile, RenameFile, DeleteFile]]]

    # A map of change annotations that can be referenced in
    # `AnnotatedTextEdit`s or create, rename and delete file / folder
    # operations.
    #
    # Whether clients honor this property depends on the client capability
    # `workspace.changeAnnotationSupport`.
    #
    # @since 3.16.0
    change_annotations: Dict[List[str], ChangeAnnotation]  # List[annotationId]: ChangeAnnotation


@dataclass
class TextDocumentItem(SerializableStructure):
    """
    Data structure which represents an item to transfer a text document from the client to the server.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocumentItem
    """
    # The text document's URI.
    uri: str

    # The text document's language identifier. See language ids in the reference for this structure.
    language_id: str

    # The version number of this document (it will increase after each change, including undo/redo).
    version: int

    # The content of the opened text document.
    text: str


@dataclass
class TextDocumentPositionParams(SerializableStructure):
    """
    Data structure which represents a parameter literal used in requests to pass a text document and a position
    inside that document.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocumentPositionParams
    """
    # The text document.
    text_document: TextDocumentIdentifier

    # The position inside the text document.
    position: Position


@dataclass
class DocumentFilter(SerializableStructure):
    """
    Data structure which represents a document filter which denotes a document through properties like language,
    scheme or pattern
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#documentFilter
    """
    # A language id, like `typescript`.
    language: Optional[str]

    # A Uri [scheme](#Uri.scheme), like `file` or `untitled`.
    scheme: Optional[str]

    # A glob pattern, like `*.{ts,js}`.
    #
    # Glob patterns can have the following syntax:
    # - `*` to match one or more characters in a path segment
    # - `?` to match on one character in a path segment
    # - `**` to match any number of path segments, including none
    # - `{}` to group sub patterns into an OR expression. (e.g. `**​/*.{ts,js}`
    #   matches all TypeScript and JavaScript files)
    # - `[]` to declare a range of characters to match in a path segment
    #   (e.g., `example.[0-9]` to match on `example.0`, `example.1`, …)
    # - `[!...]` to negate a range of characters to match in a path segment
    #   (e.g., `example.[!0-9]` to match on `example.a`, `example.b`, but
    #   not `example.0`)
    pattern: Optional[str]


class MarkupKind(Enum):
    """
    Represents a string value which content can be represented in different formats
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#markupContent
    """
    PLAINTEXT = 'plaintext'
    MARKDOWN = 'markdown'


@dataclass
class MarkupContent(SerializableStructure):
    """
    Data structure which represents a document filter which denotes a document through properties like language,
    scheme or pattern
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#markupContentInnerDefinition
    """
    # A `MarkupContent` literal represents a string value which content is
    # interpreted base on its kind flag. Currently the protocol supports
    # `plaintext` and `markdown` as markup kinds.
    #
    # If the kind is `markdown` then the value can contain fenced code blocks like
    # in GitHub issues.
    #
    # Here is an example how such a string can be constructed using
    # JavaScript / TypeScript:
    # ```typescript
    # let markdown: MarkdownContent = {
    # 	kind: MarkupKind.Markdown,
    # 	value: [
    # 		'# Header',
    # 		'Some text',
    # 		'```typescript',
    # 		'someCode();',
    # 		'```'
    # 	].join('\n')
    # };
    # ```
    #
    # *Please Note* that clients might sanitize the return markdown. A client could
    # decide to remove HTML from the markdown to avoid script execution.

    # The type of the Markup
    kind: MarkupKind

    # The content itself
    value: str


class TraceValue(Enum):
    """
    Defines the level of verbosity to trace server actions with.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#traceValue
    """
    OFF = 'off'
    MESSAGES = 'messages'
    VERBOSE = 'verbose'
