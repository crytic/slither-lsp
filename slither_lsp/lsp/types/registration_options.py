from dataclasses import dataclass, field
from enum import IntFlag
from typing import Optional, List

from slither_lsp.lsp.types.base_serializable_structure import SerializableStructure, serialization_metadata
from slither_lsp.lsp.types.basic_structures import DocumentFilter


@dataclass
class TextDocumentRegistrationOptions(SerializableStructure):
    """
    Data structure which represents general text document registration options.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocumentRegistrationOptions
    """
    documentSelector: Optional[List[DocumentFilter]] = field(
        default=None,
        metadata=serialization_metadata(include_none=True)
    )  # DocumentSelector | null


class WatchKind(IntFlag):
    """
    Represents the type of operations a server may signal to a client that it is interested in watching.
    """
    CREATE = 1
    CHANGE = 2
    DELETE = 4


@dataclass
class FileSystemWatcher(SerializableStructure):
    """
    Data structure which represents registration options for watching files.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#didChangeWatchedFilesRegistrationOptions
    """
    # The glob pattern to watch.
    #
    #  Glob patterns can have the following syntax:
    #  - `*` to match one or more characters in a path segment
    #  - `?` to match on one character in a path segment
    #  - `**` to match any number of path segments, including none
    #  - `{}` to group sub patterns into an OR expression. (e.g. `**​/*.{ts,js}`
    #    matches all TypeScript and JavaScript files)
    #  - `[]` to declare a range of characters to match in a path segment
    #    (e.g., `example.[0-9]` to match on `example.0`, `example.1`, …)
    #  - `[!...]` to negate a range of characters to match in a path segment
    #    (e.g., `example.[!0-9]` to match on `example.a`, `example.b`, but not
    #    `example.0`)
    glob_pattern: str

    # The kind of events of interest. If omitted it defaults
    # to WatchKind.Create | WatchKind.Change | WatchKind.Delete
    # which is 7.
    kind: Optional[WatchKind]


@dataclass
class DidChangeWatchedFilesRegistrationOptions(SerializableStructure):
    """
    Data structure which describe options to be used when registering for file system change events.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#didChangeWatchedFilesRegistrationOptions
    """
    # The watchers to register.
    watchers: List[FileSystemWatcher]
