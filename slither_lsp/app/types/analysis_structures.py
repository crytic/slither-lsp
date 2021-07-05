from dataclasses import dataclass
from typing import Optional

from crytic_compile import CryticCompile
from slither import Slither

from slither_lsp.app.types.compilation_structures import CompilationTarget
from slither_lsp.lsp.types.base_serializable_structure import SerializableStructure


@dataclass
class AnalysisResult:
    """
    Data structure which represents compilation and analysis results.
    """
    # Defines if our analysis succeeded
    succeeded: bool

    # Our compilation target settings
    compilation_target: CompilationTarget

    # Our compilation result
    compilation: Optional[CryticCompile]

    # Our analysis result
    analysis: Optional[Slither]

    # An exception if the operation did not succeed
    error: Optional[Exception]
