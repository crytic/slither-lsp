from typing import TYPE_CHECKING, List, Optional

import lsprotocol.types as lsp

from slither_lsp.app.utils.file_paths import uri_to_fs_path
from slither_lsp.app.utils.ranges import get_object_name_range

if TYPE_CHECKING:
    from slither_lsp.app.slither_server import SlitherServer


def register_code_lens_handlers(ls: "SlitherServer"):
    @ls.thread()
    @ls.feature(lsp.TEXT_DOCUMENT_CODE_LENS)
    def code_lens(
        ls: "SlitherServer", params: lsp.CodeLensParams
    ) -> Optional[List[lsp.CodeLens]]:
        target_filename_str: str = uri_to_fs_path(params.text_document.uri)
        res: List[lsp.CodeLens] = []
        for analysis, comp in ls.get_analyses_containing(target_filename_str):
            filename = comp.filename_lookup(target_filename_str)
            functions = [
                func
                for contract in analysis.contracts
                if contract.source_mapping
                and contract.source_mapping.filename == filename
                for func in contract.functions_and_modifiers_declared
            ]
            for func in functions:
                txt = f"SlithIR for {func.canonical_name}\n\n"
                for node in func.nodes:
                    if node.expression:
                        txt += f"Expression: {node.expression}\n"
                        txt += "IRs:\n"
                        for ir in node.irs:
                            txt += f"\t{ir}\n"
                    elif node.irs:
                        txt += "IRs:\n"
                        for ir in node.irs:
                            txt += f"\t{ir}\n"
                res.append(
                    lsp.CodeLens(
                        range=get_object_name_range(func, comp),
                        command=lsp.Command(
                            "Show SlithIR",
                            "slither.show_slithir",
                            [func.canonical_name, txt],
                        ),
                    )
                )
        return res
