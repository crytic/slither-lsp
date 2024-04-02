from enum import Enum
from typing import Any, Dict, List, Optional, Union

import attrs
from crytic_compile import CryticCompile
from slither import Slither


class CompilationTargetType(Enum):
    """
    Represents the type of target for compilation.
    """

    BASIC = "basic"
    STANDARD_JSON = "standard_json"


@attrs.define
class CompilationTargetBasic:
    """
    Data structure which represents options to compile against a basic string path target for crytic-compile.
    """

    target: str = attrs.field()
    """ The target destination for a crytic-compile target. """


@attrs.define
class CompilationTargetStandardJson:
    """
    Data structure which represents options to compile against solc standard json via crytic-compile.
    References:
        https://docs.soliditylang.org/en/latest/using-the-compiler.html#compiler-input-and-output-json-description
    """

    target: Any = attrs.field()
    """ The target destination for a crytic-compile target. """


@attrs.define
class CompilationTarget:
    """
    Data structure which represents options to compile solidity files.
    """

    target_type: CompilationTargetType = attrs.field()
    """ Defines the type of target for compilation settings. """

    target_basic: Optional[CompilationTargetBasic] = attrs.field(default=None)
    """ Defines compilation settings for a BASIC target type. """

    target_standard_json: Optional[CompilationTargetStandardJson] = attrs.field(
        default=None
    )
    """ Defines compilation settings for a STANDARD_JSON target type. """

    cwd_workspace: Optional[str] = attrs.field(default=None)
    """ Defines an optional workspace folder name to use as the working directory. """

    crytic_compile_args: Optional[Dict[str, Union[str, bool]]] = attrs.field(
        default=None
    )
    """ Additional arguments to provide to crytic-compile. """


@attrs.define
class SlitherDetectorSettings:
    """
    Data structure which represents options to show slither detector output.
    """

    enabled: bool = attrs.field(default=True)
    """ Defines whether detector output should be enabled at all """

    hidden_checks: List[str] = attrs.field(default=[])
    """ Defines a list of detector check identifiers which represent detector output we wish to suppress. """


@attrs.define
class SlitherDetectorResultElementSourceMapping:
    start: int = attrs.field()
    """ The source starting offset for this element """

    length: int = attrs.field()
    """ The source ending offset for this element """

    filename_absolute: str = attrs.field()
    """ An absolute path to the filename. """

    filename_relative: str = attrs.field()
    """ A relative path to the filename from the working directory slither was executed from. """

    filename_short: str = attrs.field()
    """ A short filepath used for display purposes. """

    lines: List[int] = attrs.field()
    """ A list of line numbers associated with the finding. """

    starting_column: int = attrs.field()
    """ The starting column of the finding, starting from the first line. """

    ending_column: int = attrs.field()
    """ The ending column of the finding, ending on the last line. """

    is_dependency: bool = attrs.field()


@attrs.define
class SlitherDetectorResultElement:
    name: str = attrs.field()
    """ The name of the source mapped item associated with a slither detector result """

    source_mapping: Optional[SlitherDetectorResultElementSourceMapping] = attrs.field()
    """ The source mapping associated with the element associated with the detector result. """

    type: str = attrs.field()
    """ The type of item this represents (contract, function, etc.) """

    @staticmethod
    def from_dict(dict):
        return SlitherDetectorResultElement(
            name=dict["name"],
            source_mapping=(
                SlitherDetectorResultElementSourceMapping(**dict["source_mapping"])
                if dict["source_mapping"]
                else None
            ),
            type=dict["type"],
        )


@attrs.define
class SlitherDetectorResult:
    """
    Data structure which represents slither detector results.
    """

    check: str = attrs.field()
    """ The detector check identifier. """

    confidence: str = attrs.field()
    """ The level of confidence in the detector result. """

    impact: str = attrs.field()
    """ The severity of the detector result if it is a true-positive. """

    description: str = attrs.field()
    """ A description of a detector result. """

    elements: List[SlitherDetectorResultElement] = attrs.field()
    """ Source mapped elements that are relevant to this detector result. """

    @staticmethod
    def from_dict(dict):
        return SlitherDetectorResult(
            check=dict["check"],
            confidence=dict["confidence"],
            impact=dict["impact"],
            description=dict["description"],
            elements=[
                SlitherDetectorResultElement.from_dict(elem)
                for elem in dict["elements"]
            ],
        )


@attrs.define
class AnalysisResult:
    """
    Data structure which represents compilation and analysis results for internal use.
    """

    succeeded: bool = attrs.field()
    """ Defines if our analysis succeeded """

    compilation: Optional[CryticCompile] = attrs.field()
    """ Our compilation result """

    analysis: Optional[Slither] = attrs.field()
    """ Our analysis result """

    error: Optional[Exception] = attrs.field()
    """ An exception if the analysis did not succeed """

    detector_results: Optional[List[SlitherDetectorResult]] = attrs.field(default=None)
    """ Detector output """
