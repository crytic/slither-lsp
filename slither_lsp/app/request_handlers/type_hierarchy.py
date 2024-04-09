from dataclasses import dataclass
from typing import TYPE_CHECKING, List, Optional, Set

import lsprotocol.types as lsp
from slither.core.declarations import Contract
from slither.utils.source_mapping import get_definition

from slither_lsp.app.utils.file_paths import fs_path_to_uri, uri_to_fs_path
from slither_lsp.app.utils.ranges import get_object_name_range

from .types import Range, to_lsp_range, to_range

if TYPE_CHECKING:
    from slither_lsp.app.slither_server import SlitherServer


@dataclass(frozen=True)
class TypeItem:
    name: str
    range: Range
    kind: lsp.SymbolKind
    filename: str
    offset: int


def register_on_prepare_type_hierarchy(ls: "SlitherServer"):
    @ls.thread()
    @ls.feature(lsp.TEXT_DOCUMENT_PREPARE_TYPE_HIERARCHY)
    def on_prepare_type_hierarchy(
        ls: "SlitherServer", params: lsp.TypeHierarchyPrepareParams
    ) -> Optional[List[lsp.TypeHierarchyItem]]:
        res: Set[TypeItem] = set()

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
                if not isinstance(obj, Contract):
                    continue
                offset = get_definition(obj, comp).start
                range_ = get_object_name_range(obj, comp)
                if obj.is_interface:
                    kind = lsp.SymbolKind.Interface
                else:
                    kind = lsp.SymbolKind.Class
                res.add(
                    TypeItem(
                        name=obj.name,
                        range=to_range(range_),
                        kind=kind,
                        filename=source.filename.absolute,
                        offset=offset,
                    )
                )
        return [
            lsp.TypeHierarchyItem(
                name=item.name,
                kind=item.kind,
                uri=fs_path_to_uri(item.filename),
                range=to_lsp_range(item.range),
                selection_range=to_lsp_range(item.range),
                data={
                    "filename": item.filename,
                    "offset": item.offset,
                },
            )
            for item in res
        ]


def register_on_get_subtypes(ls: "SlitherServer"):
    @ls.thread()
    @ls.feature(lsp.TYPE_HIERARCHY_SUBTYPES)
    def on_get_subtypes(
        ls: "SlitherServer", params: lsp.TypeHierarchySubtypesParams
    ) -> Optional[List[lsp.TypeHierarchyItem]]:
        res: Set[TypeItem] = set()

        # Obtain our filename for this file
        # These will have been populated either by
        # the initial "prepare call hierarchy" or by
        # other calls to "get incoming calls"
        target_filename_str = params.item.data["filename"]
        target_offset = params.item.data["offset"]

        referenced_contracts = [
            contract
            for analysis, _ in ls.get_analyses_containing(target_filename_str)
            for contract in analysis.offset_to_objects(
                target_filename_str, target_offset
            )
            if isinstance(contract, Contract)
        ]

        contracts = [
            (contract, analysis_result.compilation)
            for analysis_result in ls.analyses
            if analysis_result.analysis is not None
            for comp_unit in analysis_result.analysis.compilation_units
            for contract in comp_unit.contracts
        ]

        for contract in referenced_contracts:
            for other_contract, other_contract_comp in contracts:
                if contract not in other_contract.immediate_inheritance:
                    continue
                range_ = get_object_name_range(other_contract, other_contract_comp)
                if other_contract.is_interface:
                    kind = lsp.SymbolKind.Interface
                else:
                    kind = lsp.SymbolKind.Class
                item = TypeItem(
                    name=other_contract.name,
                    range=to_range(range_),
                    kind=kind,
                    filename=other_contract.source_mapping.filename.absolute,
                    offset=get_definition(other_contract, other_contract_comp).start,
                )
                res.add(item)
        return [
            lsp.TypeHierarchyItem(
                name=item.name,
                kind=item.kind,
                uri=fs_path_to_uri(item.filename),
                range=to_lsp_range(item.range),
                selection_range=to_lsp_range(item.range),
                data={
                    "filename": item.filename,
                    "offset": item.offset,
                },
            )
            for item in res
        ]


def register_on_get_supertypes(ls: "SlitherServer"):
    @ls.thread()
    @ls.feature(lsp.TYPE_HIERARCHY_SUPERTYPES)
    def on_get_supertypes(
        ls: "SlitherServer", params: lsp.TypeHierarchySupertypesParams
    ) -> Optional[List[lsp.TypeHierarchyItem]]:
        res: Set[TypeItem] = set()

        # Obtain our filename for this file
        # These will have been populated either by
        # the initial "prepare call hierarchy" or by
        # other calls to "get incoming calls"
        target_filename_str = params.item.data["filename"]
        target_offset = params.item.data["offset"]

        supertypes = [
            (supertype, comp)
            for analysis, comp in ls.get_analyses_containing(target_filename_str)
            for contract in analysis.offset_to_objects(
                target_filename_str, target_offset
            )
            if isinstance(contract, Contract)
            for supertype in contract.immediate_inheritance
        ]

        for sup, comp in supertypes:
            range_ = get_object_name_range(sup, comp)
            if sup.is_interface:
                kind = lsp.SymbolKind.Interface
            else:
                kind = lsp.SymbolKind.Class
            item = TypeItem(
                name=sup.name,
                range=to_range(range_),
                kind=kind,
                filename=sup.source_mapping.filename.absolute,
                offset=get_definition(sup, comp).start,
            )
            res.add(item)
        return [
            lsp.TypeHierarchyItem(
                name=item.name,
                kind=item.kind,
                uri=fs_path_to_uri(item.filename),
                range=to_lsp_range(item.range),
                selection_range=to_lsp_range(item.range),
                data={
                    "filename": item.filename,
                    "offset": item.offset,
                },
            )
            for item in res
        ]
