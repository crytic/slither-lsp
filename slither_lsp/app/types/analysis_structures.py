from typing import List, Optional

import attrs
from crytic_compile import CryticCompile
from slither import Slither


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
    def from_dict(dict_):
        return SlitherDetectorResultElement(
            name=dict_["name"],
            source_mapping=(
                SlitherDetectorResultElementSourceMapping(**dict_["source_mapping"])
                if dict_["source_mapping"]
                else None
            ),
            type=dict_["type"],
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
    def from_dict(dict_):
        return SlitherDetectorResult(
            check=dict_["check"],
            confidence=dict_["confidence"],
            impact=dict_["impact"],
            description=dict_["description"],
            elements=[
                SlitherDetectorResultElement.from_dict(elem)
                for elem in dict_["elements"]
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
