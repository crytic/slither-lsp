from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional, Set

import lsprotocol.types as lsp
from slither.core.declarations import Function
from slither.core.expressions import CallExpression
from slither.slithir.operations import HighLevelCall, InternalCall
from slither.utils.function import get_function_id

from slither_lsp.app.utils.file_paths import uri_to_fs_path
from slither_lsp.app.utils.ranges import get_object_name_range, source_to_range

from .types import Pos, to_lsp_pos, to_pos

if TYPE_CHECKING:
    from slither_lsp.app.slither_server import SlitherServer


@dataclass(frozen=True)
class InlayHint:
    pos: Pos
    label: str


def register_inlay_hints_handlers(ls: "SlitherServer"):
    @ls.thread()
    @ls.feature(lsp.TEXT_DOCUMENT_INLAY_HINT)
    def inlay_hints(
        ls: "SlitherServer", params: lsp.InlayHintParams
    ) -> Optional[List[lsp.InlayHint]]:
        # Obtain our filename for this file
        target_filename_str: str = uri_to_fs_path(params.text_document.uri)
        res: Set[InlayHint] = set()
        for analysis, comp in ls.get_analyses_containing(target_filename_str):
            filename = comp.filename_lookup(target_filename_str)

            contracts = [
                contract
                for contract in analysis.contracts
                if contract.source_mapping
                and contract.source_mapping.filename == filename
            ]

            #
            # Shows the ID of a function next to its definition
            #
            functions = [
                func
                for contract in contracts
                for func in contract.functions_and_modifiers_declared
            ]

            def add_id_inlay(func):
                function_id = get_function_id(func.solidity_signature)
                name_range = get_object_name_range(func, comp)
                res.add(
                    InlayHint(
                        pos=to_pos(name_range.end),
                        label=f": {function_id:#0{10}x}",
                    )
                )

            for func in functions:
                if func.visibility in {"public", "external"}:
                    add_id_inlay(func)

                for op in func.all_slithir_operations():
                    if not isinstance(op, (InternalCall, HighLevelCall)):
                        continue
                    if not isinstance(op.expression, CallExpression):
                        continue
                    if not isinstance(op.function, Function):
                        continue
                    if op.expression.names is not None:
                        # If the arguments name are already populated, this
                        # call has named fields and we can skip it
                        continue
                    for index in range(len(op.expression.arguments)):
                        arg = op.expression.arguments[index]
                        arg_name = op.function.parameters[index].name
                        pos = to_pos(source_to_range(arg.source_mapping).start)
                        res.add(
                            InlayHint(
                                pos=pos,
                                label=f"{arg_name}: ",
                            )
                        )

        return [
            lsp.InlayHint(position=to_lsp_pos(hint.pos), label=hint.label)
            for hint in res
        ]
