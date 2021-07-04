from slither_lsp.lsp.requests.base_request import BaseRequest
from slither_lsp.lsp.state.server_context import ServerContext
from slither_lsp.lsp.types.params import UnregistrationParams


class UnregisterCapabilityRequest(BaseRequest):
    """
    Request which sends a capability to a client to register for.
    """

    method_name = "client/unregisterCapability"

    @classmethod
    def send(cls, context: ServerContext, params: UnregistrationParams) -> None:
        """
        Sends a 'client/unregisterCapability' request to the client to register for new capabilities.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-current/#client_unregisterCapability
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters needed to send the request.
        :return: None
        """

        # Invoke the operation otherwise.
        context.server.send_request_message(cls.method_name, params.to_dict())

        # This request returns nothing on success.
        return None
