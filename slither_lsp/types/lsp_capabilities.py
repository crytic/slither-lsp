from dataclasses import dataclass, field
from typing import Any, Optional, Union, List

from slither_lsp.types.base_serializable_structure import SerializableStructure
from slither_lsp.types.lsp_basic_structures import DiagnosticTag


# region Server Capabilities


@dataclass
class WorkDoneProgressOptions(SerializableStructure):
    """
    Data structure which represents capabilities to see if work done progress can be tracked.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#workDoneProgressOptions
    """

    work_done_progress: Optional[bool] = None

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['work_done_progress'] = source_dict.get('workDoneProgress')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}
        if self.work_done_progress is not None:
            result['workDoneProgress'] = self.work_done_progress
        return result


@dataclass
class DeclarationOptions(WorkDoneProgressOptions):
    """
    Data structure which represents declaration options provided via capabilities.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#declarationOptions
    """
    # NOTE: This simply inherits from WorkDoneProgressOptions for now
    pass


@dataclass
class DefinitionOptions(WorkDoneProgressOptions):
    """
    Data structure which represents definition options provided via capabilities.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#definitionOptions
    """
    # NOTE: This simply inherits from WorkDoneProgressOptions for now
    pass


@dataclass
class TypeDefinitionOptions(WorkDoneProgressOptions):
    """
    Data structure which represents type definition options provided via capabilities.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#typeDefinitionOptions
    """
    # NOTE: This simply inherits from WorkDoneProgressOptions for now
    pass


@dataclass
class ImplementationOptions(WorkDoneProgressOptions):
    """
    Data structure which represents implementation options provided via capabilities.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#implementationOptions
    """
    # NOTE: This simply inherits from WorkDoneProgressOptions for now
    pass


@dataclass
class ReferenceOptions(WorkDoneProgressOptions):
    """
    Data structure which represents find reference options provided via capabilities.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#referenceOptions
    """
    # NOTE: This simply inherits from WorkDoneProgressOptions for now
    pass


@dataclass
class WorkspaceFoldersServerCapabilities(SerializableStructure):
    """
    Data structure which represents workspace folder specific server capabilities.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#workspaceFoldersServerCapabilities
    """
    # The server has support for workspace folders
    supported: Optional[bool] = None

    # Whether the server wants to receive workspace folder
    # change notifications.
    #
    # If a string is provided, the string is treated as an ID
    # under which the notification is registered on the client
    # side. The ID can be used to unregister for these events
    # using the `client/unregisterCapability` request.
    change_notifications: Union[str, bool, None] = None

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['supported'] = source_dict.get('supported')
        init_args['change_notifications'] = source_dict.get('changeNotifications')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}
        if self.supported is not None:
            result['supported'] = self.supported
        if self.change_notifications is not None:
            result['changeNotifications'] = self.change_notifications
        return result


@dataclass
class WorkspaceServerCapabilities(SerializableStructure):
    """
    Data structure which represents workspace specific server capabilities.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#serverCapabilities
    """
    workspace_folders: Optional[WorkspaceFoldersServerCapabilities] = WorkspaceFoldersServerCapabilities()

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        workspace_folders = source_dict.get('workspaceFolders')
        if workspace_folders is not None:
            workspace_folders = WorkspaceFoldersServerCapabilities.from_dict(workspace_folders)
        init_args['workspace_folders'] = workspace_folders

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}

        if self.workspace_folders is not None:
            result['workspaceFolders'] = self.workspace_folders.to_dict()

        return result


@dataclass
class ServerCapabilities(SerializableStructure):
    """
    Data structure which represents capabilities a server supports.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#serverCapabilities
    """

    # The server provides go to declaration support.
    # @since 3.14.0
    # TODO: Once we add DeclarationRegistrationOptions, we need to add logic for it here, as it should be another
    #  possible value type for this field.
    declaration_provider: Union[bool, DeclarationOptions, None] = None

    # The server provides goto definition support.
    definition_provider: Union[bool, DefinitionOptions, None] = None

    # The server provides goto type definition support.
    # @since 3.6.0
    # TODO: Once we add TypeDefinitionRegistrationOptions, we need to add logic for it here, as it should be another
    #  possible value type for this field.
    type_definition_provider: Union[bool, TypeDefinitionOptions, None] = None

    # The server provides goto implementation support.
    # @since 3.6.0
    # TODO: Once we add ImplementationRegistrationOptions, we need to add logic for it here, as it should be another
    #  possible value type for this field.
    implementation_provider: Union[bool, ImplementationOptions, None] = None

    # The server provides find references support.
    references_provider: Union[bool, ReferenceOptions, None] = None

    # Workspace specific server capabilities
    workspace: Optional[WorkspaceServerCapabilities] = WorkspaceServerCapabilities()

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        # Read declaration provider capabilities. If it's a dictionary, it likely represents a DeclarationOptions or
        # DeclarationRegistrationOptions, otherwise, it should be a bool which we still accept.
        declaration_provider = source_dict.get('declarationProvider')
        if declaration_provider is not None and isinstance(declaration_provider, dict):
            declaration_provider = DeclarationOptions.from_dict(declaration_provider)
        init_args['declaration_provider'] = declaration_provider

        # Read definitions provider capabilities. If it's a dictionary, it likely represents a DefinitionOptions.
        # Otherwise, it should be a bool which we still accept.
        definition_provider = source_dict.get('definitionProvider')
        if definition_provider is not None and isinstance(definition_provider, dict):
            definition_provider = DefinitionOptions.from_dict(definition_provider)
        init_args['definition_provider'] = definition_provider

        # Read type definition provider capabilities. If it's a dictionary, it likely represents TypeDefinitionOptions
        # or TypeDefinitionRegistrationOptions. Otherwise, it should be a bool which we still accept.
        type_definition_provider = source_dict.get('typeDefinitionProvider')
        if type_definition_provider is not None and isinstance(type_definition_provider, dict):
            type_definition_provider = TypeDefinitionOptions.from_dict(type_definition_provider)
        init_args['type_definition_provider'] = type_definition_provider

        # Read implementation provider capabilities. If it's a dictionary, it likely represents a ImplementationOptions
        # or a ImplementationRegistrationOptions. Otherwise, it should be a bool which we still accept.
        implementation_provider = source_dict.get('implementationProvider')
        if implementation_provider is not None and isinstance(implementation_provider, dict):
            implementation_provider = ImplementationOptions.from_dict(implementation_provider)
        init_args['implementation_provider'] = implementation_provider

        # Read find references provider capabilities. If it's a dictionary, it likely represents ReferenceOptions.
        # Otherwise, it should be a bool which we still accept.
        references_provider = source_dict.get('referencesProvider')
        if references_provider is not None and isinstance(references_provider, dict):
            references_provider = ReferenceOptions.from_dict(references_provider)
        init_args['references_provider'] = references_provider

        # Read workspace information
        workspace = source_dict.get('workspace')
        if workspace is not None:
            workspace = WorkspaceServerCapabilities.from_dict(workspace)
        init_args['workspace'] = workspace

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}

        # Declaration provider is handled accordingly based on type.
        if self.declaration_provider is not None:
            if isinstance(self.declaration_provider, bool):
                result['declarationProvider'] = self.declaration_provider
            elif isinstance(self.declaration_provider, DeclarationOptions):
                result['declarationProvider'] = self.declaration_provider.to_dict()

        # Definition provider is handled accordingly based on type.
        if self.definition_provider is not None:
            if isinstance(self.definition_provider, bool):
                result['definitionProvider'] = self.definition_provider
            elif isinstance(self.definition_provider, DefinitionOptions):
                result['definitionProvider'] = self.definition_provider.to_dict()

        # Type Definition provider is handled accordingly based on type.
        if self.type_definition_provider is not None:
            if isinstance(self.type_definition_provider, bool):
                result['typeDefinitionProvider'] = self.type_definition_provider
            elif isinstance(self.type_definition_provider, TypeDefinitionOptions):
                result['typeDefinitionProvider'] = self.type_definition_provider.to_dict()

        # Implementation provider is handled accordingly based on type.
        if self.implementation_provider is not None:
            if isinstance(self.implementation_provider, bool):
                result['implementationProvider'] = self.implementation_provider
            elif isinstance(self.implementation_provider, ImplementationOptions):
                result['implementationProvider'] = self.implementation_provider.to_dict()

        # Find references provider is handled accordingly based on type.
        if self.references_provider is not None:
            if isinstance(self.references_provider, bool):
                result['referencesProvider'] = self.references_provider
            elif isinstance(self.references_provider, ReferenceOptions):
                result['referencesProvider'] = self.references_provider.to_dict()

        # Output our workspace information
        if self.workspace is not None:
            result['workspace'] = self.workspace.to_dict()
        return result

# endregion


# region Client Capabilities

@dataclass
class ShowDocumentClientCapabilities(SerializableStructure):
    """
    Data structure which represents capabilities for the request to display a document.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#window_showDocument
    """
    # The client has support for the show document request.
    support: bool = False

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['support'] = source_dict.get('support')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}
        result['support'] = self.support
        return result


@dataclass
class WindowClientCapabilities(SerializableStructure):
    """
     Data structure which represents window specific client capabilities.
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#clientCapabilities
    """
    # Whether client supports handling progress notifications. If set
    # servers are allowed to report in `workDoneProgress` property in the
    # request specific server capabilities.
    # @since 3.15.0
    work_done_progress: Optional[bool] = None

    # TODO: showMessage

    # Client capabilities for the show document request.
    # @since 3.16.0
    show_document: Optional[ShowDocumentClientCapabilities] = None

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['work_done_progress'] = source_dict.get('workDoneProgress')
        show_document = source_dict.get('showDocument')
        if show_document is not None:
            show_document = ShowDocumentClientCapabilities.from_dict(show_document)
        init_args['show_document'] = show_document

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}

        if self.work_done_progress is not None:
            result['workDoneProgress'] = self.work_done_progress
        if self.show_document is not None:
            result['showDocument'] = self.show_document.to_dict()

        return result


@dataclass
class PublishDiagnosticsTagSupportClientCapabilities(SerializableStructure):
    """
     Data structure which contains tag support information ('tagSupport' in 'PublishDiagnosticsClientCapabilities')
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#publishDiagnosticsClientCapabilities
    """
    # Whether the clients accepts diagnostics with related information.
    value_set: List[DiagnosticTag] = field(default_factory=list)

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        value_set: List[int] = source_dict.get('valueSet')
        if value_set is not None:
            value_set = [DiagnosticTag(v) for v in value_set]
        init_args['value_set'] = value_set

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}

        if self.value_set is not None:
            result['valueSet'] = self.value_set

        return result


@dataclass
class PublishDiagnosticsClientCapabilities(SerializableStructure):
    """
     Data structure which represents text document specific client capabilities.
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#publishDiagnosticsClientCapabilities
    """
    # Whether the clients accepts diagnostics with related information.
    related_information: Optional[bool] = None

    # Client supports the tag property to provide meta data about a diagnostic.
    # Clients supporting tags have to handle unknown tags gracefully.
    # @since 3.15.0
    tag_support: Optional[PublishDiagnosticsTagSupportClientCapabilities] = None

    # Whether the client interprets the version property of the
    # `textDocument/publishDiagnostics` notification's parameter.
    # @since 3.15.0
    version_support: Optional[bool] = None

    # Client supports a codeDescription property
    # @since 3.16.0
    code_description_support: Optional[bool] = None

    # Whether code action supports the `data` property which is
    # preserved between a `textDocument/publishDiagnostics` and
    # `textDocument/codeAction` request.
    # @since 3.16.0
    data_support: Optional[bool] = None

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['related_information'] = source_dict.get('relatedInformation')

        tag_support = source_dict.get('tagSupport')
        if tag_support is not None:
            tag_support = PublishDiagnosticsTagSupportClientCapabilities.from_dict(tag_support)
        init_args['tag_support'] = tag_support

        init_args['version_support'] = source_dict.get('versionSupport')
        init_args['code_description_support'] = source_dict.get('codeDescriptionSupport')
        init_args['data_support'] = source_dict.get('dataSupport')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}

        if self.related_information is not None:
            result['relatedInformation'] = self.related_information
        if self.tag_support is not None:
            result['tagSupport'] = self.tag_support.to_dict()
        if self.version_support is not None:
            result['versionSupport'] = self.version_support
        if self.code_description_support is not None:
            result['codeDescriptionSupport'] = self.code_description_support
        if self.data_support is not None:
            result['dataSupport'] = self.data_support

        return result


@dataclass
class DeclarationClientCapabilities(SerializableStructure):
    """
     Data structure which contains capabilities specific to the 'textDocument/declaration' request.
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocumentClientCapabilities
    """
    # Whether declaration supports dynamic registration. If this is set to
    # `true` the client supports the new `DeclarationRegistrationOptions`
    # return value for the corresponding server capability as well.
    dynamic_registration: Optional[bool] = None

    # The client supports additional metadata in the form of declaration links.
    link_support: Optional[bool] = None

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['dynamic_registration'] = source_dict.get('dynamicRegistration')
        init_args['link_support'] = source_dict.get('linkSupport')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}

        if self.dynamic_registration is not None:
            result['valueSet'] = self.dynamic_registration
        if self.link_support is not None:
            result['linkSupport'] = self.link_support

        return result


@dataclass
class DefinitionClientCapabilities(SerializableStructure):
    """
     Data structure which contains capabilities specific to the 'textDocument/definition' request.
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#definitionClientCapabilities
    """
    # Whether definition supports dynamic registration.
    dynamic_registration: Optional[bool] = None

    # The client supports additional metadata in the form of definition links.
    # @since 3.14.0
    link_support: Optional[bool] = None

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['dynamic_registration'] = source_dict.get('dynamicRegistration')
        init_args['link_support'] = source_dict.get('linkSupport')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}

        if self.dynamic_registration is not None:
            result['valueSet'] = self.dynamic_registration
        if self.link_support is not None:
            result['linkSupport'] = self.link_support

        return result


@dataclass
class TypeDefinitionClientCapabilities(SerializableStructure):
    """
     Data structure which contains capabilities specific to the 'textDocument/typeDefinition' request.
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#typeDefinitionClientCapabilities
    """
    # Whether implementation supports dynamic registration. If this is set to
    # `true` the client supports the new `TypeDefinitionRegistrationOptions`
    # return value for the corresponding server capability as well.
    dynamic_registration: Optional[bool] = None

    # The client supports additional metadata in the form of definition links.
    # @since 3.14.0
    link_support: Optional[bool] = None

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['dynamic_registration'] = source_dict.get('dynamicRegistration')
        init_args['link_support'] = source_dict.get('linkSupport')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}

        if self.dynamic_registration is not None:
            result['valueSet'] = self.dynamic_registration
        if self.link_support is not None:
            result['linkSupport'] = self.link_support

        return result


@dataclass
class ImplementationClientCapabilities(SerializableStructure):
    """
     Data structure which contains capabilities specific to the 'textDocument/implementation' request.
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#implementationClientCapabilities
    """
    # Whether implementation supports dynamic registration. If this is set to
    # `true` the client supports the new `ImplementationRegistrationOptions`
    # return value for the corresponding server capability as well.
    dynamic_registration: Optional[bool] = None

    # The client supports additional metadata in the form of definition links.
    # @since 3.14.0
    link_support: Optional[bool] = None

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['dynamic_registration'] = source_dict.get('dynamicRegistration')
        init_args['link_support'] = source_dict.get('linkSupport')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}

        if self.dynamic_registration is not None:
            result['valueSet'] = self.dynamic_registration
        if self.link_support is not None:
            result['linkSupport'] = self.link_support

        return result


@dataclass
class ReferenceClientCapabilities(SerializableStructure):
    """
     Data structure which contains capabilities specific to the 'textDocument/references' request.
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#referenceClientCapabilities
    """
    # Whether references supports dynamic registration.
    dynamic_registration: Optional[bool] = None

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['dynamic_registration'] = source_dict.get('dynamicRegistration')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}

        if self.dynamic_registration is not None:
            result['valueSet'] = self.dynamic_registration

        return result


@dataclass
class TextDocumentClientCapabilities(SerializableStructure):
    """
     Data structure which represents text document specific client capabilities.
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#textDocumentClientCapabilities
    """
    # Capabilities specific to the `textDocument/declaration` request.
    # @since 3.14.0
    declaration: Optional[DeclarationClientCapabilities] = None

    # Capabilities specific to the `textDocument/definition` request.
    definition: Optional[DefinitionClientCapabilities] = None

    # Capabilities specific to the `textDocument/typeDefinition` request.
    # @since 3.6.0
    type_definition: Optional[TypeDefinitionClientCapabilities] = None

    # Capabilities specific to the `textDocument/implementation` request.
    # @since 3.6.0
    implementation: Optional[ImplementationClientCapabilities] = None

    # Capabilities specific to the `textDocument/references` request.
    references: Optional[ReferenceClientCapabilities] = None

    # Capabilities specific to the `textDocument/publishDiagnostics` notification.
    publish_diagnostics: Optional[PublishDiagnosticsClientCapabilities] = None

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        declaration = source_dict.get('declaration')
        if declaration is not None:
            declaration = DeclarationClientCapabilities.from_dict(declaration)
        init_args['declaration'] = declaration

        definition = source_dict.get('definition')
        if definition is not None:
            definition = DefinitionClientCapabilities.from_dict(definition)
        init_args['definition'] = definition

        type_definition = source_dict.get('typeDefinition')
        if type_definition is not None:
            type_definition = TypeDefinitionClientCapabilities.from_dict(type_definition)
        init_args['type_definition'] = type_definition

        implementation = source_dict.get('implementation')
        if implementation is not None:
            implementation = ImplementationClientCapabilities.from_dict(implementation)
        init_args['implementation'] = implementation

        references = source_dict.get('references')
        if references is not None:
            references = ReferenceClientCapabilities.from_dict(references)
        init_args['references'] = references

        publish_diagnostics = source_dict.get('publishDiagnostics')
        if publish_diagnostics is not None:
            publish_diagnostics = PublishDiagnosticsClientCapabilities.from_dict(publish_diagnostics)
        init_args['publish_diagnostics'] = publish_diagnostics

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}

        if self.declaration is not None:
            result['declaration'] = self.declaration.to_dict()
        if self.definition is not None:
            result['definition'] = self.definition.to_dict()
        if self.type_definition is not None:
            result['typeDefinition'] = self.type_definition.to_dict()
        if self.implementation is not None:
            result['implementation'] = self.implementation.to_dict()
        if self.references is not None:
            result['references'] = self.references.to_dict()

        if self.publish_diagnostics is not None:
            result['publishDiagnostics'] = self.publish_diagnostics.to_dict()

        return result


@dataclass
class WorkspaceClientCapabilities(SerializableStructure):
    """
     Data structure which represents workspace specific client capabilities.
     References:
         https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#clientCapabilities
     """
    # The client supports applying batch edits
    # to the workspace by supporting the request
    # 'workspace/applyEdit'
    apply_edit: Optional[bool] = None

    # TODO: workspaceEdit, didChangeConfiguration, didChangeWatchedFiles, symbol, executeCommand

    # The client has support for workspace folders.
    # @since 3.6.0
    workspace_folders: Optional[bool] = None

    # The client supports `workspace/configuration` requests.
    # @since 3.6.0
    configuration: Optional[bool] = None

    # TODO: semanticTokens, codeLens, fileOperations, textDocument, window, general,

    # Experimental client capabilities.
    experimental: Any = None

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        init_args['apply_edit'] = source_dict.get('applyEdit')
        init_args['workspace_folders'] = source_dict.get('workspaceFolders')
        init_args['configuration'] = source_dict.get('configuration')
        init_args['experimental'] = source_dict.get('experimental')

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}

        if self.apply_edit is not None:
            result['applyEdit'] = self.apply_edit
        if self.workspace_folders is not None:
            result['workspaceFolders'] = self.workspace_folders
        if self.configuration is not None:
            result['configuration'] = self.configuration
        if self.experimental is not None:
            result['experimental'] = self.experimental

        return result


@dataclass
class ClientCapabilities(SerializableStructure):
    """
    Data structure which represents capabilities a client supports.
    References:
        https://microsoft.github.io/language-server-protocol/specifications/specification-3-17/#clientCapabilities
    """
    # Workspace specific client capabilities.
    workspace: Optional[WorkspaceClientCapabilities] = WorkspaceClientCapabilities()

    # Window specific client capabilities.
    window: Optional[WindowClientCapabilities] = WindowClientCapabilities()

    # Text document specific client capabilities.
    text_document: Optional[TextDocumentClientCapabilities] = TextDocumentClientCapabilities()

    @classmethod
    def _init_args_from_dict(cls, init_args: dict, source_dict: dict) -> None:
        """
        Parses dataclass arguments into an argument dictionary which is used to instantiate the underlying class.
        :param init_args: The arguments dictionary which this function populates, to be later used to create an instance
        of the item, where each key corresponds to the a dataclass field.
        :return: None
        """
        workspace = source_dict.get('workspace')
        if workspace is not None:
            workspace = WorkspaceClientCapabilities.from_dict(workspace)
        init_args['workspace'] = workspace

        window = source_dict.get('window')
        if window is not None:
            window = WindowClientCapabilities.from_dict(window)
        init_args['window'] = window

        text_document = source_dict.get('textDocument')
        if text_document is not None:
            text_document = TextDocumentClientCapabilities.from_dict(text_document)
        init_args['text_document'] = text_document

    def to_dict(self, result: Optional[dict] = None) -> Any:
        """
        Dumps an instance of this class to a dictionary object.
        :return: Returns a dictionary object that represents an instance of this data.
        """
        result = result if result is not None else {}

        if self.workspace is not None:
            result['workspace'] = self.workspace.to_dict()
        if self.window is not None:
            result['window'] = self.window.to_dict()
        if self.text_document is not None:
            result['textDocument'] = self.text_document.to_dict()

        return result

# endregion
