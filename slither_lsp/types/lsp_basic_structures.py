from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import IntEnum, Enum
from typing import Optional, Any, Union, List

# These structures ideally would just be dataclass objects, so we could cast dictionaries to dataclasses.
# However, dataclasses cannot initialize with unexpected parameters, and we can't assume the Language Server
# Protocol won't change and add more keys. So we handle parsing ourselves for now.
# See more at the link below:
# https://microsoft.github.io/language-server-protocol/specifications/specification-current/#basic-json-structures

# Text documents have a defined EOL.
# https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocuments
EOL = ['\n', '\r\n', '\r']


@dataclass
class ClientServerInfo:
    """
    Data structure which describes a client/server by name and version.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#initialize
    """
    # The name of the client/server as defined by itself.
    name: str

    # The client/server's version as defined by itself.
    version: Optional[str]

    @classmethod
    def from_dict(cls, obj: dict) -> 'ClientServerInfo':
        """
        Parses the provided object into an instance of the class.
        :param obj: The dictionary object to parse this structure from.
        :return: Returns an instance of the class.
        """
        name: str = obj.get('name')
        version: Optional[str] = obj.get('version')
        return cls(name=name, version=version)

    def to_dict(self) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Set our mandatory fields
        result = {
            "name": self.name
        }

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
class WorkspaceFolder:
    """
    Data structure which describes a workspace folder by name and location (uri).
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#workspaceFolder
    """
    # The associated URI for this workspace folder.
    uri: str

    # The name of the workspace folder. Used to refer to this
    # workspace folder in the user interface.
    name: Optional[str]

    @classmethod
    def from_dict(cls, obj: dict) -> 'WorkspaceFolder':
        """
        Parses the provided object into an instance of the class.
        :param obj: The dictionary object to parse this structure from.
        :return: Returns an instance of the class.
        """
        uri: str = obj.get('uri')
        name: str = obj.get('name')
        return cls(uri=uri, name=name)

    def to_dict(self) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        return {
            'uri': self.uri,
            'name': self.name
        }


@dataclass
class Position:
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
    def from_dict(cls, obj: dict) -> 'Position':
        """
        Parses the provided object into an instance of the class.
        :param obj: The dictionary object to parse this structure from.
        :return: Returns an instance of the class.
        """
        line: int = obj.get('line')
        character: int = obj.get('character')
        return cls(line=line, character=character)

    def to_dict(self) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        return {
            'line': self.line,
            'character': self.character
        }


@dataclass
class Range:
    """
    Data structure which represents a position range in a text file.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#range
    """
    start: Position
    end: Position

    @classmethod
    def from_dict(cls, obj: dict) -> 'Range':
        """
        Parses the provided object into an instance of the class.
        :param obj: The dictionary object to parse this structure from.
        :return: Returns an instance of the class.
        """
        start = Position.from_dict(obj.get('start'))
        end = Position.from_dict(obj.get('end'))
        return cls(start=start, end=end)

    def to_dict(self) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        return {
            'start': self.start.to_dict(),
            'end': self.end.to_dict()
        }


@dataclass
class Location:
    """
    Data structure which represents a text file location (file uri and position range).
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#location
    """
    uri: str
    range: Range

    @classmethod
    def from_dict(cls, obj: dict) -> 'Location':
        """
        Parses the provided object into an instance of the class.
        :param obj: The dictionary object to parse this structure from.
        :return: Returns an instance of the class.
        """
        location_uri: str = obj.get('uri')
        location_range = Range.from_dict(obj.get('range'))
        return cls(uri=location_uri, range=location_range)

    def to_dict(self) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        return {
            'uri': self.uri,
            'range': self.range.to_dict()
        }


@dataclass
class LocationLink:
    """
    Data structure which represents a link between a source and target destination.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#locationLink
    """
    # Span of the origin of the link.
    # Used as the underlined span for mouse interaction. Defaults to the word
    # range at the mouse position.
    origin_selection_range: Optional[Range]

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

    @classmethod
    def from_dict(cls, obj: dict) -> 'LocationLink':
        """
        Parses the provided object into an instance of the class.
        :param obj: The dictionary object to parse this structure from.
        :return: Returns an instance of the class.
        """
        # Parse the optional origin selection range
        ll_origin_selection_range: dict = obj.get('originSelectionRange')
        ll_origin_selection_range: Optional[Range] = \
            Range.from_dict(ll_origin_selection_range) if ll_origin_selection_range is not None else None

        # Parse the remainder of our variables
        ll_target_uri = obj.get('targetUri')
        ll_target_range = Range.from_dict(obj.get('targetRange'))
        ll_target_selection_range = Range.from_dict(obj.get('targetSelectionRange'))
        return cls(
            origin_selection_range=ll_origin_selection_range, target_uri=ll_target_uri, target_range=ll_target_range,
            target_selection_range=ll_target_selection_range
        )

    def to_dict(self) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Set our mandatory fields
        result = {
            'targetUri': self.target_uri,
            'targetRange': self.target_range.to_dict(),
            'targetSelectionRange': self.target_selection_range.to_dict(),
        }

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
class DiagnosticRelatedInformation:
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
    def from_dict(cls, obj: dict) -> 'DiagnosticRelatedInformation':
        """
        Parses the provided object into an instance of the class.
        :param obj: The dictionary object to parse this structure from.
        :return: Returns an instance of the class.
        """
        location: Location = Location.from_dict(obj.get('location'))
        message: str = obj.get('message')
        return cls(location=location, message=message)

    def to_dict(self) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        return {
            'location': self.location.to_dict(),
            'message': self.message
        }


@dataclass
class CodeDescription:
    """
    Data structure which represents a description for an error code.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#codeDescription
    """
    href: str

    @classmethod
    def from_dict(cls, obj: dict) -> 'CodeDescription':
        """
        Parses the provided object into an instance of the class.
        :param obj: The dictionary object to parse this structure from.
        :return: Returns an instance of the class.
        """
        href: str = obj.get('href')
        return cls(href=href)

    def to_dict(self) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        return {
            'href': self.href
        }


@dataclass
class Diagnostic:
    """
    Data structure which represents a diagnostic (compiler error, warning, etc). Diagnostic objects are only valid
    in the scope of a resource.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#diagnostic
    """
    # The range at which the message applies.
    range: Range

    # The diagnostic's severity. Can be omitted. If omitted it is up to the
    # client to interpret diagnostics as error, warning, info or hint.
    severity: Optional[DiagnosticSeverity]

    # The diagnostic's code, which might appear in the user interface.
    code: Union[int, str, None]

    # An optional property to describe the error code.
    code_description: Optional[CodeDescription]

    # A human-readable string describing the source of this
    # diagnostic, e.g. 'typescript' or 'super lint'.
    source: Optional[str]

    # The diagnostic's message.
    message: str

    # Additional metadata about the diagnostic.
    tags: Optional[List[DiagnosticTag]]

    # An array of related diagnostic information, e.g. when symbol-names within
    # a scope collide all definitions can be marked via this property.
    related_information: Optional[List[DiagnosticRelatedInformation]]

    # A data entry field that is preserved between a
    # `textDocument/publishDiagnostics` notification and
    # `textDocument/codeAction` request.
    data: Any

    @classmethod
    def from_dict(cls, obj: dict) -> 'Diagnostic':
        """
        Parses the provided object into an instance of the class.
        :param obj: The dictionary object to parse this structure from.
        :return: Returns an instance of the class.
        """
        d_range: Range = Range.from_dict(obj.get('range'))

        d_severity: Optional[int] = obj.get('severity')
        d_severity: Optional[DiagnosticSeverity] = DiagnosticSeverity(d_severity) if d_severity is not None else None

        d_code: Union[int, str, None] = obj.get('code')

        d_code_description: Optional[dict] = obj.get('codeDescription')
        d_code_description: Optional[CodeDescription] = \
            CodeDescription.from_dict(d_code_description) if d_code_description is not None else None

        d_source: Optional[str] = obj.get('source')
        d_message: str = obj.get('message')

        d_tags: Optional[List[int]] = obj.get('tags')
        d_tags: Optional[List[DiagnosticTag]] = \
            [DiagnosticTag(d_tag) for d_tag in d_tags] \
            if d_tags is not None and isinstance(d_tags, list) \
            else None

        d_related_information: Optional[List[dict]] = obj.get('relatedInformation')
        d_related_information: Optional[List[DiagnosticRelatedInformation]] = \
            [DiagnosticRelatedInformation.from_dict(info_item) for info_item in d_related_information] \
            if d_related_information is not None and isinstance(d_related_information, list) \
            else None

        d_data: Any = obj.get('data')

        return cls(
            range=d_range, severity=d_severity, code=d_code, code_description=d_code_description, source=d_source,
            message=d_message, tags=d_tags, related_information=d_related_information, data=d_data
        )

    def to_dict(self) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Set our mandatory fields
        result = {
            'range': self.range.to_dict(),
            'message': self.message
        }

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
class Command:
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
    arguments: Optional[List[Any]]

    @classmethod
    def from_dict(cls, obj: dict) -> 'Command':
        """
        Parses the provided object into an instance of the class.
        :param obj: The dictionary object to parse this structure from.
        :return: Returns an instance of the class.
        """
        title: str = obj.get('title')
        command: str = obj.get('command')
        arguments: Optional[List[Any]] = obj.get('arguments')

        return cls(title=title, command=command, arguments=arguments)

    def to_dict(self) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Set our mandatory fields
        result = {
            'title': self.title,
            'command': self.command
        }

        # Set optional fields
        if self.arguments is not None:
            result['arguments'] = self.arguments

        # Return the result.
        return result


@dataclass
class TextEdit:
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
    def from_dict(cls, obj: dict) -> 'TextEdit':
        """
        Parses the provided object into an instance of the class.
        :param obj: The dictionary object to parse this structure from.
        :return: Returns an instance of the class.
        """
        te_range = Range.from_dict(obj.get('range'))
        te_new_text: str = obj.get('newText')

        return cls(range=te_range, new_text=te_new_text)

    def to_dict(self) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Set our mandatory fields
        result = {
            'range': self.range.to_dict(),
            'newText': self.new_text
        }

        # Return the result.
        return result


@dataclass
class ChangeAnnotation:
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
    needs_confirmation: Optional[bool]

    # A human-readable string which is rendered less prominent in
    # the user interface.
    description: Optional[str]

    @classmethod
    def from_dict(cls, obj: dict) -> 'ChangeAnnotation':
        """
        Parses the provided object into an instance of the class.
        :param obj: The dictionary object to parse this structure from.
        :return: Returns an instance of the class.
        """
        label: str = obj.get('label')
        needs_confirmation: Optional[bool] = obj.get('needsConfirmation')
        description: Optional[str] = obj.get('description')

        return cls(label=label, needs_confirmation=needs_confirmation, description=description)

    def to_dict(self) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Set our mandatory fields
        result = {
            'label': self.label
        }

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
    def from_dict(cls, obj: dict) -> 'AnnotatedTextEdit':
        """
        Parses the provided object into an instance of the class.
        :param obj: The dictionary object to parse this structure from.
        :return: Returns an instance of the class.
        """
        ate_range = Range.from_dict(obj.get('range'))
        ate_new_text: str = obj.get('newText')
        ate_annotation_id = obj.get('annotationId')

        return cls(range=ate_range, new_text=ate_new_text, annotation_id=ate_annotation_id)

    def to_dict(self) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        # Set our base fields
        result = super().to_dict()

        # Set our additional fields
        result['annotationId'] = self.annotation_id

        # Return the result.
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
