from collections import defaultdict
from dataclasses import dataclass
from typing import TYPE_CHECKING, Dict, List, Optional, Set, Tuple

import lsprotocol.types as lsp
from slither.core.declarations import Function
from slither.slithir.operations import HighLevelCall, InternalCall
from slither.utils.source_mapping import get_definition

from slither_lsp.app.utils.file_paths import fs_path_to_uri, uri_to_fs_path
from slither_lsp.app.utils.ranges import (
    get_object_name_range,
    source_to_range,
)

from .types import Range, to_lsp_range, to_range

if TYPE_CHECKING:
    from slither_lsp.app.slither_server import SlitherServer


@dataclass(frozen=True)
class CallItem:
    name: str
    range: Range
    filename: str
    offset: int


def register_on_prepare_call_hierarchy(ls: "SlitherServer"):
    @ls.thread()
    @ls.feature(lsp.TEXT_DOCUMENT_PREPARE_CALL_HIERARCHY)
    def on_prepare_call_hierarchy(
        ls: "SlitherServer", params: lsp.CallHierarchyPrepareParams
    ) -> Optional[List[lsp.CallHierarchyItem]]:
        """
        `textDocument/prepareCallHierarchy` doesn't actually produce
        the call hierarchy in this case, it only detects what objects
        we are trying to produce the call hierarchy for.
        The data returned from this method will be sent by the client
        back to the "get incoming/outgoing calls" later.
        """
        res: Dict[Tuple[str, int], lsp.CallHierarchyItem] = {}

        # Obtain our filename for this file
        target_filename_str: str = uri_to_fs_path(params.text_document.uri)

        for analysis, comp in ls.get_analyses_containing(target_filename_str):
            # Obtain the offset for this line + character position
            target_offset = comp.get_global_offset_from_line(
                target_filename_str, params.position.line + 1
            )
            # Obtain objects
            objects = analysis.offset_to_objects(
                target_filename_str, target_offset + params.position.character
            )
            for obj in objects:
                source = obj.source_mapping
                if not isinstance(obj, Function):
                    continue
                offset = get_definition(obj, comp).start
                res[(target_filename_str, offset)] = lsp.CallHierarchyItem(
                    name=obj.canonical_name,
                    kind=lsp.SymbolKind.Function,
                    uri=fs_path_to_uri(source.filename.absolute),
                    range=source_to_range(source),
                    selection_range=get_object_name_range(obj, comp),
                    data={
                        "filename": target_filename_str,
                        "offset": offset,
                    },
                )
        return [elem for elem in res.values()]


def register_on_get_incoming_calls(ls: "SlitherServer"):
    @ls.thread()
    @ls.feature(lsp.CALL_HIERARCHY_INCOMING_CALLS)
    def on_get_incoming_calls(
        ls: "SlitherServer", params: lsp.CallHierarchyIncomingCallsParams
    ) -> Optional[List[lsp.CallHierarchyIncomingCall]]:
        res: Dict[CallItem, Set[Range]] = defaultdict(set)

        # Obtain our filename for this file
        # These will have been populated either by
        # the initial "prepare call hierarchy" or by
        # other calls to "get incoming calls"
        target_filename_str = params.item.data["filename"]
        target_offset = params.item.data["offset"]

        referenced_functions = [
            obj
            for analysis, comp in ls.get_analyses_containing(target_filename_str)
            for obj in analysis.offset_to_objects(target_filename_str, target_offset)
            if isinstance(obj, Function)
        ]

        calls = [
            (f, op, analysis_result.compilation)
            for analysis_result in ls.analyses
            if analysis_result.analysis is not None
            for comp_unit in analysis_result.analysis.compilation_units
            for f in comp_unit.functions
            for op in f.all_slithir_operations()
            if isinstance(op, (InternalCall, HighLevelCall))
            and isinstance(op.function, Function)
        ]

        for func in referenced_functions:
            for call_from, call, call_comp in calls:
                if call.function is not func:
                    continue
                expr_range = source_to_range(call.expression.source_mapping)
                func_range = source_to_range(call_from.source_mapping)
                item = CallItem(
                    name=call_from.canonical_name,
                    range=to_range(func_range),
                    filename=call_from.source_mapping.filename.absolute,
                    offset=get_definition(call_from, call_comp).start,
                )
                res[item].add(to_range(expr_range))
        return [
            lsp.CallHierarchyIncomingCall(
                from_=lsp.CallHierarchyItem(
                    name=call_from.name,
                    kind=lsp.SymbolKind.Function,
                    uri=fs_path_to_uri(call_from.filename),
                    range=to_lsp_range(call_from.range),
                    selection_range=to_lsp_range(call_from.range),
                    data={
                        "filename": call_from.filename,
                        "offset": call_from.offset,
                    },
                ),
                from_ranges=[to_lsp_range(range) for range in ranges],
            )
            for (call_from, ranges) in res.items()
        ]


def register_on_get_outgoing_calls(ls: "SlitherServer"):
    @ls.thread()
    @ls.feature(lsp.CALL_HIERARCHY_OUTGOING_CALLS)
    def on_get_outgoing_calls(
        ls: "SlitherServer", params: lsp.CallHierarchyOutgoingCallsParams
    ) -> Optional[List[lsp.CallHierarchyOutgoingCall]]:
        res: Dict[CallItem, Set[Range]] = defaultdict(set)

        # Obtain our filename for this file
        target_filename_str = params.item.data["filename"]
        target_offset = params.item.data["offset"]

        for analysis, comp in ls.get_analyses_containing(target_filename_str):
            objects = analysis.offset_to_objects(target_filename_str, target_offset)
            for obj in objects:
                if not isinstance(obj, Function):
                    continue
                calls = [
                    op
                    for op in obj.all_slithir_operations()
                    if isinstance(op, (InternalCall, HighLevelCall))
                ]
                for call in calls:
                    if not isinstance(call.function, Function):
                        continue
                    call_to = call.function
                    expr_range = source_to_range(call.expression.source_mapping)
                    func_range = source_to_range(call_to.source_mapping)
                    item = CallItem(
                        name=call_to.canonical_name,
                        range=to_range(func_range),
                        filename=call_to.source_mapping.filename.absolute,
                        offset=get_definition(call_to, comp).start,
                    )
                    res[item].add(to_range(expr_range))

        return [
            lsp.CallHierarchyOutgoingCall(
                to=lsp.CallHierarchyItem(
                    name=call_to.name,
                    kind=lsp.SymbolKind.Function,
                    uri=fs_path_to_uri(call_to.filename),
                    range=to_lsp_range(call_to.range),
                    selection_range=to_lsp_range(call_to.range),
                    data={
                        "filename": call_to.filename,
                        "offset": call_to.offset,
                    },
                ),
                from_ranges=[to_lsp_range(range) for range in ranges],
            )
            for (call_to, ranges) in res.items()
        ]
