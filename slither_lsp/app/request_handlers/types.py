from typing import TypeAlias, Tuple
import lsprotocol.types as lsp

# Type definitions for call hierarchy
Pos: TypeAlias = Tuple[int, int]
Range: TypeAlias = Tuple[Pos, Pos]


def to_lsp_pos(pos: Pos) -> lsp.Position:
    return lsp.Position(line=pos[0], character=pos[1])


def to_lsp_range(range_: Range) -> lsp.Range:
    return lsp.Range(start=to_lsp_pos(range_[0]), end=to_lsp_pos(range_[1]))


def to_pos(pos: lsp.Position) -> Pos:
    return (pos.line, pos.character)


def to_range(range_: lsp.Range) -> Range:
    return (to_pos(range_.start), to_pos(range_.end))
