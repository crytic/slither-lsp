from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Union, Any, List, Dict

from crytic_compile import CryticCompile
from slither import Slither
from slither_lsp.lsp.types.base_serializable_structure import SerializableStructure, serialization_metadata


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
class SlitherDetectorSettings(SerializableStructure):
    """
    Data structure which represents options to show slither detector output.
    """
    # Defines whether detector output should be enabled at all
    enabled: bool = True

    # Defines a list of detector check identifiers which represent detector output we wish to suppress.
    hidden_checks: List[str] = field(default_factory=list)


@dataclass
class SlitherDetectorResultElementSourceMapping(SerializableStructure):
    # The source starting offset for this element
    start: int

    # The source ending offset for this element
    length: int

    # An absolute path to the filename.
    filename_absolute: str = field(metadata=serialization_metadata(name_override='filename_absolute'))

    # A relative path to the filename from the working directory slither was executed from.
    filename_relative: str = field(metadata=serialization_metadata(name_override='filename_relative'))

    # A short filepath used for display purposes.
    filename_short: str = field(metadata=serialization_metadata(name_override='filename_short'))

    # The filename used by slither
    filename_used: str = field(metadata=serialization_metadata(name_override='filename_used'))

    # A list of line numbers associated with the finding.
    lines: List[int]

    # The starting column of the finding, starting from the first line.
    starting_column: int = field(metadata=serialization_metadata(name_override='starting_column'))

    # The ending column of the finding, ending on the last line.
    ending_column: int = field(metadata=serialization_metadata(name_override='ending_column'))


@dataclass
class SlitherDetectorResultElement(SerializableStructure):
    # The name of the source mapped item associated with a slither detector result
    name: str

    # The source mapping associated with the element associated with the detector result.
    source_mapping: Optional[SlitherDetectorResultElementSourceMapping] = field(metadata=serialization_metadata(name_override='source_mapping'))

    # The type of item this represents (contract, function, etc.)
    type: str

    # The fields related to this element type.
    type_specific_fields: Any = field(metadata=serialization_metadata(name_override='type_specific_fields'))

    # Any additional detector-specific field.
    additional_fields: Any = field(metadata=serialization_metadata(name_override='additional_fields'))


@dataclass
class SlitherDetectorResult(SerializableStructure):
    """
    Data structure which represents slither detector results.
    """
    # The detector check identifier.
    check: str

    # The level of confidence in the detector result.
    confidence: str

    # The severity of the detector result if it is a true-positive.
    impact: str

    # A description of a detector result.
    description: str

    # Source mapped elements that are relevant to this detector result.
    elements: List[SlitherDetectorResultElement]

    # Any additional detector-specific field.
    additional_fields: Any = field(metadata=serialization_metadata(name_override='additional_fields'))


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

    # An exception if the analysis did not succeed
    error: Optional[Exception]

    # Detector output
    detector_results: Optional[List[SlitherDetectorResult]] = None
