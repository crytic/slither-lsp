from dataclasses import dataclass
from enum import Enum
from typing import Optional, Union, Any, List, Dict

from crytic_compile import CryticCompile
from slither import Slither
from slither_lsp.lsp.types.base_serializable_structure import SerializableStructure


class CompilationTargetType(Enum):
    """
    Represents the type of target for compilation.
    """
    BASIC = 'basic'
    STANDARD_JSON = 'standard_json'


@dataclass
class CompilationTargetBasic(SerializableStructure):
    """
    Data structure which represents options to compile against a basic string path target for crytic-compile.
    """
    # The target destination for a crytic-compile target.
    target: str


@dataclass
class CompilationTargetStandardJson(SerializableStructure):
    """
    Data structure which represents options to compile against solc standard json via crytic-compile.
    References:
        https://docs.soliditylang.org/en/latest/using-the-compiler.html#compiler-input-and-output-json-description
    """
    # The target destination for a crytic-compile target.
    target: Any


@dataclass
class CompilationTarget(SerializableStructure):
    """
    Data structure which represents options to compile solidity files.
    """
    # Defines the type of target for compilation settings.
    target_type: CompilationTargetType

    # Defines compilation settings for a BASIC target type.
    target_basic: Optional[CompilationTargetBasic] = None

    # Defines compilation settings for a STANDARD_JSON target type.
    target_standard_json: Optional[CompilationTargetStandardJson] = None

    # Defines an optional workspace folder name to use as the working directory.
    cwd_workspace: Optional[str] = None

    # Additional arguments to provide to crytic-compile.
    crytic_compile_args: Optional[Dict[str, Union[str, bool]]] = None


@dataclass
class AnalysisResult:
    """
    Data structure which represents compilation and analysis results for internal use.
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