from typing import Any

from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.requests.client.register_capability import RegisterCapabilityRequest
from slither_lsp.lsp.state.server_context import ServerContext
from slither_lsp.lsp.types.errors import CapabilitiesNotSupportedError
from slither_lsp.lsp.types.params import DidChangeWatchedFilesParams, RegistrationParams, Registration, Unregistration
from slither_lsp.lsp.types.registration_options import DidChangeWatchedFilesRegistrationOptions


class DidChangeWatchedFilesHandler(BaseRequestHandler):
    """
    Handler for the 'workspace/didChangeWatchedFiles' notification, which notifies the server that the client
    detected changes to files which the server previously requested be watched.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#workspace_didChangeWatchedFiles
    """

    method_name = "workspace/didChangeWatchedFiles"

    @classmethod
    def get_registration(cls, context: ServerContext, registration_id: str,
                         registration_options: DidChangeWatchedFilesRegistrationOptions) -> Registration:
        """
        Obtains an Registration object to be used with a 'client/registerCapability' request given a set of
        registration options.
        :param context: The server context which determines the server to use to send the message.
        :param registration_id: The identifier to assign this capability registration to, to be used for later
        unregistration.
        :param registration_options: The options to provide for this capability registration.
        :return: The Registration object.
        """
        # Verify we have appropriate capabilities.
        if context.client_capabilities.workspace is None or \
                context.client_capabilities.workspace.did_change_watched_files is None or \
                context.client_capabilities.workspace.did_change_watched_files.dynamic_registration is not True:
            raise CapabilitiesNotSupportedError(
                request_or_handler=cls,
                additional_text="Could not dynamically register for these capabilities because the client does not "
                                "support dynamic registration."
            )

        return Registration(id=registration_id, method=cls.method_name, register_options=registration_options)

    @classmethod
    def get_unregistration(cls, context: ServerContext, registration_id: str) -> Unregistration:
        """
        Obtains an Unregistration object given a previously registered capability registration id.
        :param context: The server context which determines the server to use to send the message.
        :param registration_id: A previously registered capability registration id.
        :return: The Unregistration to be used with a 'client/unregisterCapability' request.
        """
        # Verify we have appropriate capabilities.
        if context.client_capabilities.workspace is None or \
                context.client_capabilities.workspace.did_change_watched_files is None or \
                context.client_capabilities.workspace.did_change_watched_files.dynamic_registration is not True:
            raise CapabilitiesNotSupportedError(
                request_or_handler=cls,
                additional_text="Could not dynamically register for these capabilities because the client does not "
                                "support dynamic registration."
            )

        return Unregistration(id=registration_id, method=cls.method_name)

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        """
        Handles a 'workspace/didChangeWatchedFiles' notification which notifies the server that the client
        detected changes to files which the server previously requested be watched.
        References:
            https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#workspace_didChangeWatchedFiles
        :param context: The server context which determines the server to use to send the message.
        :param params: The parameters object provided with this message.
        :return: None
        """

        # Validate the structure of our request
        params: DidChangeWatchedFilesParams = DidChangeWatchedFilesParams.from_dict(params)

        # Emit relevant events
        context.event_emitter.emit(
            'workspace.didChangeWatchedFiles',
            params=params
        )

        # This is a notification so we return nothing
        return None
