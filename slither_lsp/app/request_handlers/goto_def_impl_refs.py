# pylint: disable=broad-exception-caught

from typing import TYPE_CHECKING, Callable, List, Optional, Set

import lsprotocol.types as lsp
from slither import Slither
from slither.core.source_mapping.source_mapping import Source

from slither_lsp.app.utils.file_paths import uri_to_fs_path
from slither_lsp.app.utils.ranges import source_to_location

if TYPE_CHECKING:
    from slither_lsp.app.slither_server import SlitherServer


def _inspect_analyses(
    ls: "SlitherServer",
    target_filename_str: str,
    line: int,
    col: int,
    func: Callable[[Slither, int], Set[Source]],
) -> List[lsp.Location]:
    # Compile a list of definitions
    results = []

    # Loop through all compilations
    for analysis_result in ls.analyses:
        if analysis_result.analysis is not None:
            # TODO: Remove this temporary try/catch once we refactor crytic-compile to now throw errors in
            #  these functions.
            try:
                # Obtain the offset for this line + character position
                target_offset = analysis_result.compilation.get_global_offset_from_line(
                    target_filename_str, line
                )
                # Obtain sources
                sources = func(analysis_result.analysis, target_offset + col)
            except Exception:
                continue
            else:
                # Add all definitions from this source.
                for source in sources:
                    source_location: Optional[lsp.Location] = source_to_location(source)
                    if source_location is not None:
                        results.append(source_location)

    return results


def register_on_goto_definition(ls: "SlitherServer"):
    @ls.thread()
    @ls.feature(lsp.TEXT_DOCUMENT_DEFINITION)
    def on_goto_definition(
        ls: "SlitherServer", params: lsp.DefinitionParams
    ) -> List[lsp.Location]:
        # Obtain our filename for this file
        target_filename_str: str = uri_to_fs_path(params.text_document.uri)

        return _inspect_analyses(
            ls,
            target_filename_str,
            params.position.line + 1,
            params.position.character,
            lambda analysis, offset: analysis.offset_to_definitions(
                target_filename_str, offset
            ),
        )


def register_on_goto_implementation(ls: "SlitherServer"):
    @ls.thread()
    @ls.feature(lsp.TEXT_DOCUMENT_IMPLEMENTATION)
    def on_goto_implementation(
        ls: "SlitherServer", params: lsp.ImplementationParams
    ) -> List[lsp.Location]:
        # Obtain our filename for this file
        target_filename_str: str = uri_to_fs_path(params.text_document.uri)

        return _inspect_analyses(
            ls,
            target_filename_str,
            params.position.line + 1,
            params.position.character,
            lambda analysis, offset: analysis.offset_to_implementations(
                target_filename_str, offset
            ),
        )


def register_on_find_references(ls: "SlitherServer"):
    @ls.thread()
    @ls.feature(lsp.TEXT_DOCUMENT_REFERENCES)
    def on_find_references(
        ls: "SlitherServer", params: lsp.ImplementationParams
    ) -> Optional[List[lsp.Location]]:
        # Obtain our filename for this file
        target_filename_str: str = uri_to_fs_path(params.text_document.uri)

        return _inspect_analyses(
            ls,
            target_filename_str,
            params.position.line + 1,
            params.position.character,
            lambda analysis, offset: analysis.offset_to_references(
                target_filename_str, offset
            ),
        )
