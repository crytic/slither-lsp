from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import IntEnum, Enum
from typing import Optional, Any, Union, List

# These structures ideally would just be dataclass objects, so we could cast dictionaries to dataclasses.
# However, dataclasses cannot initialize with unexpected parameters, and we can't assume the Language Server
# Protocol won't change and add more keys. So we add our own serializing/deserializing methods on top of
# this while still reaping benefits of auto-constructor generation, parameter validation, etc from dataclass.
# See more at the link below:
# https://microsoft.github.io/language-server-protocol/specifications/specification-current/#basic-json-structures

# Text documents have a defined EOL.
# https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocuments
from slither_lsp.types.base_serializable_structure import SerializableStructure

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

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['name'] = source_dict.get('name')
        init_args['version'] = source_dict.get('version')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create a result dictionary if we don't have one
        result = result if result is not None else {}

        # Set our mandatory fields
        result['name'] = self.name

        # Set optional fields
        if self.version is not None:
            result["version"] = self.version

        # Return the result.
        return result


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

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['uri'] = source_dict.get('uri')
        init_args['name'] = source_dict.get('name')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create a result dictionary if we don't have one
        result = result if result is not None else {}

        # Set our values and return the result
        result['uri'] = self.uri
        result['name'] = self.name
        return result


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

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['line'] = source_dict.get('line')
        init_args['character'] = source_dict.get('character')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create a result dictionary if we don't have one and set our fields
        result = result if result is not None else {}
        result['line'] = self.line
        result['character'] = self.character
        return result


@dataclass
class Range(SerializableStructure):
    """
    Data structure which represents a position range in a text file.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#range
    """
    start: Position
    end: Position

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['start'] = Position.from_dict(source_dict.get('start'))
        init_args['end'] = Position.from_dict(source_dict.get('end'))

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create a result dictionary if we don't have one and set our fields
        result = result if result is not None else {}
        result['start'] = self.start.to_dict()
        result['end'] = self.end.to_dict()
        return result


@dataclass
class Location(SerializableStructure):
    """
    Data structure which represents a text file location (file uri and position range).
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#location
    """
    uri: str
    range: Range

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['uri'] = source_dict.get('uri')
        init_args['range'] = Range.from_dict(source_dict.get('range'))

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create a result dictionary if we don't have one and set our fields
        result = result if result is not None else {}
        result['uri'] = self.uri
        result['range'] = self.range.to_dict()
        return result


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

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        # Read our optional selection range
        ll_origin_selection_range: dict = source_dict.get('originSelectionRange')
        ll_origin_selection_range: Optional[Range] = \
            Range.from_dict(ll_origin_selection_range) if ll_origin_selection_range is not None else None

        # Read the remainder of our fields
        init_args['origin_selection_range'] = ll_origin_selection_range
        init_args['target_uri'] = source_dict.get('targetUri')
        init_args['target_range'] = Range.from_dict(source_dict.get('targetRange'))
        init_args['target_selection_range'] = Range.from_dict(source_dict.get('targetSelectionRange'))

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create a result dictionary if we don't have one and set our mandatory fields.
        result = result if result is not None else {}
        result['targetUri'] = self.target_uri
        result['targetRange'] = self.target_range.to_dict()
        result['targetSelectionRange'] = self.target_selection_range.to_dict()

        # Set optional fields
        if self.origin_selection_range is not None:
            result['originSelectionRange'] = self.origin_selection_range.to_dict()

        # Return the result.
        return result


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

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['location'] = Location.from_dict(source_dict.get('location'))
        init_args['message'] = source_dict.get('message')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create a result dictionary if we don't have one and set our fields
        result = result if result is not None else {}
        result['location'] = self.location.to_dict()
        result['message'] = self.message
        return result


@dataclass
class CodeDescription(SerializableStructure):
    """
    Data structure which represents a description for an error code.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#codeDescription
    """
    href: str

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['href'] = source_dict.get('href')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create a result dictionary if we don't have one and set our fields
        result = result if result is not None else {}
        result['href'] = self.href
        return result


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

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['range'] = Range.from_dict(source_dict.get('range'))

        d_severity: Optional[int] = source_dict.get('severity')
        init_args['severity'] = DiagnosticSeverity(d_severity) if d_severity is not None else None

        init_args['code'] = source_dict.get('code')

        d_code_description: Optional[dict] = source_dict.get('codeDescription')
        init_args['code_description'] = \
            CodeDescription.from_dict(d_code_description) if d_code_description is not None else None

        init_args['source'] = source_dict.get('source')
        init_args['message'] = source_dict.get('message')

        d_tags: Optional[List[int]] = source_dict.get('tags')
        init_args['tags'] = \
            [DiagnosticTag(d_tag) for d_tag in d_tags] \
            if d_tags is not None and isinstance(d_tags, list) \
            else None

        d_related_information: Optional[List[dict]] = source_dict.get('relatedInformation')
        init_args['related_information'] = \
            [DiagnosticRelatedInformation.from_dict(info_item) for info_item in d_related_information] \
            if d_related_information is not None and isinstance(d_related_information, list) \
            else None

        init_args['data'] = source_dict.get('data')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create a result dictionary if we don't have one and set our mandatory fields
        result = result if result is not None else {}
        result['range'] = self.range.to_dict()
        result['message'] = self.message

        # Set optional fields
        if self.severity is not None:
            result['severity'] = int(self.severity)
        if self.code is not None:
            result['code'] = self.code
        if self.code_description is not None:
            result['codeDescription'] = self.code_description.to_dict()
        if self.source is not None:
            result['source'] = self.source
        if self.tags is not None and isinstance(self.tags, list):
            result['tags'] = [int(tag) for tag in self.tags]
        if self.related_information is not None and isinstance(self.related_information, list):
            result['relatedInformation'] = [info_item.to_dict() for info_item in self.related_information]
        if self.data is not None:
            result['data'] = self.data

        # Return the result.
        return result


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

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['title'] = source_dict.get('title')
        init_args['command'] = source_dict.get('command')
        init_args['arguments'] = source_dict.get('arguments')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create a result dictionary if we don't have one and set our fields
        result = result if result is not None else {}
        result['title'] = self.title
        result['command'] = self.command

        # Set optional fields
        if self.arguments is not None:
            result['arguments'] = self.arguments

        # Return the result.
        return result


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

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['range'] = Range.from_dict(source_dict.get('range'))
        init_args['new_text'] = source_dict.get('newText')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create a result dictionary if we don't have one and set our fields
        result = result if result is not None else {}
        result['range'] = self.range.to_dict()
        result['newText'] = self.new_text

        # Return the result.
        return result


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

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['label'] = source_dict.get('label')
        init_args['needs_confirmation'] = source_dict.get('needsConfirmation')
        init_args['description'] = source_dict.get('description')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create a result dictionary if we don't have one and set our fields
        result = result if result is not None else {}
        result['label'] = self.label

        # Set optional fields
        if self.needs_confirmation is not None:
            result['needsConfirmation'] = self.needs_confirmation
        if self.description is not None:
            result['description'] = self.description

        # Return the result.
        return result


@dataclass
class AnnotatedTextEdit(TextEdit):
    """
    Data structure which represents a special text edit with an additional change annotation.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#annotatedTextEdit
    """

    # The actual annotation identifier.
    annotation_id: str

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        # Initialize our baseclass arguments.
        TextEdit._init_args_from_dict(init_args=init_args, source_dict=source_dict)

        # Parse our annotation id
        init_args['annotation_id'] = source_dict.get('annotationId')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create a result dictionary if we don't have one and set our fields
        result = result if result is not None else {}

        # Set our base fields to this result dict
        TextEdit.to_dict(self, result)

        # Set our additional fields
        result['annotationId'] = self.annotation_id

        # Return the result.
        return result


@dataclass
class TextDocumentIdentifier(TextEdit):
    """
    Data structure which represents a text document identifier (uri).
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocumentIdentifier
    """

    # The actual annotation identifier.
    uri: str

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['uri'] = source_dict.get('uri')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Create a result dictionary if we don't have one and set our fields
        result = result if result is not None else {}
        result['uri'] = self.uri
        return result


class TraceValue(Enum):
    """
    Defines the level of verbosity to trace server actions with.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#traceValue
    """
    OFF = 'off'
    MESSAGES = 'messages'
    VERBOSE = 'verbose'
