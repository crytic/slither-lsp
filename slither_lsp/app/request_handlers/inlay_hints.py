from typing import TYPE_CHECKING, List, Optional

import lsprotocol.types as lsp
from slither.utils.function import get_function_id

from slither_lsp.app.utils.file_paths import uri_to_fs_path
from slither_lsp.app.utils.ranges import get_object_name_range

if TYPE_CHECKING:
    from slither_lsp.app.slither_server import SlitherServer


def register_inlay_hints_handlers(ls: "SlitherServer"):
    @ls.thread()
    @ls.feature(lsp.TEXT_DOCUMENT_INLAY_HINT)
    def inlay_hints(
        ls: "SlitherServer", params: lsp.InlayHintParams
    ) -> Optional[List[lsp.InlayHint]]:
        """
        Shows the ID of a function next to its definition
        """
        # Obtain our filename for this file
        target_filename_str: str = uri_to_fs_path(params.text_document.uri)
        res: List[lsp.InlayHint] = []
        for analysis, comp in ls.get_analyses_containing(target_filename_str):
            filename = comp.filename_lookup(target_filename_str)

            functions = [
                func
                for contract in analysis.contracts
                if contract.source_mapping
                and contract.source_mapping.filename == filename
                for func in contract.functions_and_modifiers_declared
                if func.visibility in {"public", "external"}
            ]

            for func in functions:
                function_id = get_function_id(func.solidity_signature)
                name_range = get_object_name_range(func, comp)
                res.append(
                    lsp.InlayHint(
                        position=lsp.Position(
                            name_range.end.line, name_range.end.character
                        ),
                        label=f": {function_id:#0{10}x}",
                    )
                )
        return res
