from dataclasses import dataclass
from typing import Optional


@dataclass
class ClientInfo:
    name: Optional[str]
    version: Optional[str]


@dataclass
class WorkspaceFolder:
    name: Optional[str]
    uri: str
