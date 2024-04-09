# pylint: disable=too-many-branches

from typing import TYPE_CHECKING, List, Optional

import lsprotocol.types as lsp

from slither_lsp.app.utils.file_paths import uri_to_fs_path
from slither_lsp.app.utils.ranges import get_object_name_range, source_to_range

if TYPE_CHECKING:
    from slither_lsp.app.slither_server import SlitherServer


def register_symbols_handlers(ls: "SlitherServer"):
    @ls.thread()
    @ls.feature(lsp.TEXT_DOCUMENT_DOCUMENT_SYMBOL)
    def document_symbol(
        ls: "SlitherServer", params: lsp.DocumentSymbolParams
    ) -> Optional[List[lsp.DocumentSymbol]]:
        """
        Allows navigation using VSCode "breadcrumbs"
        """
        # Obtain our filename for this file
        target_filename_str: str = uri_to_fs_path(params.text_document.uri)
        res: List[lsp.DocumentSymbol] = []

        def add_child(children, obj, kind):
            children.append(
                lsp.DocumentSymbol(
                    name=obj.name,
                    kind=kind,
                    range=source_to_range(obj.source_mapping),
                    selection_range=get_object_name_range(obj, comp),
                )
            )

        for analysis, comp in ls.get_analyses_containing(target_filename_str):
            filename = comp.filename_lookup(target_filename_str)

            for contract in analysis.contracts:
                if (
                    not contract.source_mapping
                    or contract.source_mapping.filename != filename
                ):
                    continue
                if contract.is_interface:
                    kind = lsp.SymbolKind.Interface
                else:
                    kind = lsp.SymbolKind.Class
                children: List[lsp.DocumentSymbol] = []

                for struct in contract.structures_declared:
                    if struct.source_mapping is None:
                        continue
                    add_child(children, struct, lsp.SymbolKind.Struct)

                for enum in contract.enums_declared:
                    if enum.source_mapping is None:
                        continue
                    add_child(children, enum, lsp.SymbolKind.Enum)

                for event in contract.events_declared:
                    if event.source_mapping is None:
                        continue
                    add_child(children, event, lsp.SymbolKind.Enum)

                for func in contract.functions_and_modifiers_declared:
                    if func.source_mapping is None:
                        continue
                    add_child(children, func, lsp.SymbolKind.Function)

                res.append(
                    lsp.DocumentSymbol(
                        name=contract.name,
                        kind=kind,
                        range=source_to_range(contract.source_mapping),
                        selection_range=get_object_name_range(contract, comp),
                        children=children,
                    )
                )

        return res
