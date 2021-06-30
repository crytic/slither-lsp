from dataclasses import dataclass, field
from typing import Optional, List, Type

from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.state.server_hooks import ServerHooks
from slither_lsp.lsp.types.capabilities import ServerCapabilities


@dataclass
class ServerConfig:
    """
    Represents of set of configuration variables which can be passed to a server to initialize it with.
    """
    # The initial capabilities this server will broadcast to clients. This can be changed with dynamic registration
    # requests after a connection is established.
    initial_server_capabilities: ServerCapabilities

    # Hooks which can be used to fulfill language feature requests.
    hooks: Optional[ServerHooks] = None

    # List of additional request handlers to register with the server
    additional_request_handlers: List[Type[BaseRequestHandler]] = field(default_factory=list)
