from typing import Union, List, Optional, Set

from crytic_compile.utils.naming import Filename

from slither_lsp.app.utils.file_paths import uri_to_fs_path, fs_path_to_uri
from slither_lsp.lsp.state.server_context import ServerContext
from slither_lsp.lsp.state.server_hooks import ServerHooks
from slither_lsp.lsp.types.basic_structures import Location, LocationLink, Range, Position
from slither_lsp.lsp.types.params import ImplementationParams, TypeDefinitionParams, DefinitionParams, DeclarationParams
from slither.core.source_mapping.source_mapping import Source


class SlitherLSPHooks(ServerHooks):
    """
    Defines a set of hooks to fulfill core language feature requests for the Language Server Protocol, leveraging
    slither for analysis.
    """
    def __init__(self, app):
        # Late import to avoid circular reference issues
        from slither_lsp.app.app import SlitherLSPApp

        # Set our parameters.
        self.app: SlitherLSPApp = app

    @staticmethod
    def _source_to_location(source: Source) -> Optional[Location]:
        """
        Converts a slither Source mapping object into a Language Server Protocol Location.
        :param source: The slither Source mapping object to convert into a Location.
        :return: Returns a Location representing the slither Source mapping object. None if no valid mapping exists.
        """
        # If there are no mapped lines, we don't return a location.
        if len(source.lines) == 0:
            return None

        # Otherwise we can return a location fairly easily.
        return Location(
            uri=fs_path_to_uri(source.filename.absolute),
            range=Range(
                start=Position(
                    line=source.lines[0] - 1,
                    character=source.starting_column - 1
                ),
                end=Position(
                    line=source.lines[-1] - 1,
                    character=source.ending_column - 1
                )
            )
        )

    def goto_declaration(self, context: ServerContext, params: DeclarationParams) \
            -> Union[Location, List[Location], List[LocationLink], None]:
        return None

    def goto_definition(self, context: ServerContext, params: DefinitionParams) \
            -> Union[Location, List[Location], List[LocationLink], None]:
        # Compile a list of definitions
        definitions = []

        # Loop through all compilations
        with self.app.workspace.analyses_lock:
            for analysis_result in self.app.workspace.analyses:
                if analysis_result.analysis is not None:
                    # TODO: Remove this temporary try/catch once we refactor crytic-compile to now throw errors in
                    #  these functions.
                    try:
                        # Obtain our filename for this file
                        target_filename_str: str = uri_to_fs_path(params.text_document.uri)
                        target_filename = analysis_result.compilation.filename_lookup(target_filename_str)

                        # Obtain the offset for this line + character position
                        target_offset = analysis_result.compilation.get_global_offset_from_line_and_character(
                            target_filename,
                            params.position.line + 1,
                            params.position.character + 1
                        )

                        # Obtain sources
                        sources: Set[Source] = analysis_result.analysis.offset_to_definitions(
                            target_filename_str,
                            target_offset
                        )
                    except Exception:
                        continue

                    # Add all definitions from this source.
                    for source in sources:
                        source_location: Optional[Location] = self._source_to_location(source)
                        if source_location is not None:
                            definitions.append(source_location)

        return definitions

    def goto_type_definition(self, context: ServerContext, params: TypeDefinitionParams) \
            -> Union[Location, List[Location], List[LocationLink], None]:
        return None

    def goto_implementation(self, context: ServerContext, params: ImplementationParams) \
            -> Union[Location, List[Location], List[LocationLink], None]:
        return None

    def find_references(self, context: ServerContext, params: ImplementationParams) \
            -> Optional[List[Location]]:
        # Compile a list of references
        references = []

        # Loop through all compilations
        with self.app.workspace.analyses_lock:
            for analysis_result in self.app.workspace.analyses:
                if analysis_result.analysis is not None:
                    # TODO: Remove this temporary try/catch once we refactor crytic-compile to now throw errors in
                    #  these functions.
                    try:
                        # Obtain our filename for this file
                        target_filename_str: str = uri_to_fs_path(params.text_document.uri)
                        target_filename = analysis_result.compilation.filename_lookup(target_filename_str)

                        # Obtain the offset for this line + character position
                        target_offset = analysis_result.compilation.get_global_offset_from_line_and_character(
                            target_filename,
                            params.position.line + 1,
                            params.position.character + 1
                        )

                        # Obtain sources
                        sources: Set[Source] = analysis_result.analysis.offset_to_references(
                            target_filename_str,
                            target_offset
                        )
                    except Exception:
                        continue

                    # Add all references from this source.
                    for source in sources:
                        source_location: Optional[Location] = self._source_to_location(source)
                        if source_location is not None:
                            references.append(source_location)

        return references
