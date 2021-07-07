from slither_lsp.app.types.params import AnalysisProgressParams
from slither_lsp.lsp.requests.base_request import BaseRequest
from slither_lsp.lsp.state.server_context import ServerContext


class ReportAnalysisProgressNotification(BaseRequest):
    """
    Notification which sends analysis results to a client.
    """

    method_name = "$/analysis/reportAnalysisProgress"

    @classmethod
    def send(cls, context: ServerContext, params: AnalysisProgressParams) -> None:
        """
        Sends a notification to the client to report progress on analysis parameters.
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters needed to send the request.
        :return: None
        """

        # Invoke the operation otherwise.
        context.server.send_notification_message(cls.method_name, params.to_dict())

        # This is a notification so we return nothing.
        return None
