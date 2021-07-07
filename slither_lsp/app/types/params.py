from dataclasses import dataclass, field
from typing import Optional, List

from slither_lsp.app.types.analysis_structures import CompilationTarget
from slither_lsp.lsp.types.base_serializable_structure import SerializableStructure, serialization_metadata


@dataclass
class SetCompilationTargetsParams(SerializableStructure):
    """
    Data structure which represents parameters used to set compilation targets
    """
    # Represents the list of compilation targets to compile and analyze. If empty, auto-compilation will be used.
    targets: List[CompilationTarget]


@dataclass
class AnalysisResultProgress(SerializableStructure):
    """
    Data structure which represents an individual compilation and analysis result which is sent to a client.
    """
    # Defines if our analysis succeeded. If None/null, indicates analysis is still pending.
    succeeded: Optional[bool] = field(metadata=serialization_metadata(include_none=True))

    # Our compilation target settings
    compilation_target: CompilationTarget

    # An exception if the operation did not succeed
    error: Optional[str]


@dataclass
class AnalysisProgressParams(SerializableStructure):
    """
    Data structure which represents compilation and analysis results which are communicated to the client.
    """
    # A list of analysis results, one for each compilation target.
    results: List[AnalysisResultProgress]
