from typing import Union

import lsprotocol.types as lsp
from crytic_compile.crytic_compile import CryticCompile
from slither.core.declarations import (
    Contract,
    Enum,
    Event,
    Function,
    Structure,
)
from slither.core.source_mapping.source_mapping import Source
from slither.utils.source_mapping import get_definition
from slither_lsp.app.utils.file_paths import fs_path_to_uri


def source_to_range(source: Source) -> lsp.Range:
    """
    Converts a slither Source mapping object into a Language Server Protocol Location.
    :param source: The slither Source mapping object to convert into a Location.
    :return: Returns a Location representing the slither Source mapping object.
    """

    # Otherwise we can return a location fairly easily.
    return lsp.Range(
        start=lsp.Position(
            line=source.lines[0] - 1,
            character=max(0, source.starting_column - 1),
        ),
        end=lsp.Position(
            line=source.lines[-1] - 1,
            character=max(0, source.ending_column - 1),
        ),
    )


def source_to_location(source: Source) -> lsp.Location:
    """
    Converts a slither Source mapping object into a Language Server Protocol Location.
    :param source: The slither Source mapping object to convert into a Location.
    :return: Returns a Location representing the slither Source mapping object.
    """

    # Otherwise we can return a location fairly easily.
    return lsp.Location(
        uri=fs_path_to_uri(source.filename.absolute),
        range=source_to_range(source),
    )


def get_object_name_range(
    obj: Union[Function, Contract, Enum, Event, Structure], comp: CryticCompile
) -> lsp.Range:
    name_pos = get_definition(obj, comp)
    return lsp.Range(
        start=lsp.Position(
            line=name_pos.lines[0] - 1,
            character=name_pos.starting_column - 1,
        ),
        end=lsp.Position(
            line=name_pos.lines[0] - 1,
            character=name_pos.starting_column + len(obj.name) - 1,
        ),
    )
