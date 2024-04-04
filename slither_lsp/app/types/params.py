from typing import List, Optional, Union

import attrs
from slither_lsp.app.types.analysis_structures import (
    CompilationTarget,
    SlitherDetectorSettings,
)


@attrs.define
class AnalysisRequestParams:
    uris: Optional[List[str]] = attrs.field()


@attrs.define
class SetCompilationTargetsParams:
    """
    Data structure which represents parameters used to set compilation targets
    """

    targets: List[CompilationTarget] = attrs.field()
    """ Represents the list of compilation targets to compile and analyze. If empty, auto-compilation will be used. """


@attrs.define
class AnalysisResultProgress:
    """
    Data structure which represents an individual compilation and analysis result which is sent to a client.
    """

    succeeded: Optional[bool] = attrs.field()
    """ Defines if our analysis succeeded. If None/null, indicates analysis is still pending. """

    compilation_target: CompilationTarget = attrs.field()
    """ Our compilation target settings """

    error: Optional[str] = attrs.field()
    """ An exception if the operation did not succeed """


@attrs.define
class AnalysisProgressParams:
    """
    Data structure which represents compilation and analysis results which are communicated to the client.
    """

    results: List[AnalysisResultProgress] = attrs.field()
    """ A list of analysis results, one for each compilation target. """


SLITHER_ANALYZE = "$/slither/analyze"
SLITHER_GET_DETECTOR_LIST = "$/slither/getDetectorList"
SLITHER_GET_VERSION = "$/slither/getVersion"
SLITHER_SET_DETECTOR_SETTINGS = "$/slither/setDetectorSettings"
CRYTIC_COMPILE_SOLC_STANDARD_JSON_AUTOGENERATE = (
    "$/cryticCompile/solcStandardJson/autogenerate"
)
CRYTIC_COMPILE_GET_COMMAND_LINE_ARGUMENTS = "$/cryticCompile/getCommandLineArguments"
ANALYSIS_REPORT_ANALYSIS_PROGRESS = "$/analysis/reportAnalysisProgress"
COMPILATION_SET_COMPILATION_TARGETS = "$/compilation/setCompilationTargets"


@attrs.define
class SetDetectorSettingsRequest:
    id: Union[int, str] = attrs.field()
    params: SlitherDetectorSettings = attrs.field()
    method: str = SLITHER_SET_DETECTOR_SETTINGS
    jsonrpc: str = attrs.field(default="2.0")


@attrs.define
class SetCompilationTargetsRequest:
    id: Union[int, str] = attrs.field()
    params: SetCompilationTargetsParams = attrs.field()
    method: str = COMPILATION_SET_COMPILATION_TARGETS
    jsonrpc: str = attrs.field(default="2.0")


@attrs.define
class ReportAnalysisProgressNotification:
    params: AnalysisProgressParams = attrs.field()
    method: str = ANALYSIS_REPORT_ANALYSIS_PROGRESS
    jsonrpc: str = attrs.field(default="2.0")


METHOD_TO_TYPES = {
    # Requests
    SLITHER_SET_DETECTOR_SETTINGS: (
        SetDetectorSettingsRequest,
        None,
        SlitherDetectorSettings,
        None,
    ),
    COMPILATION_SET_COMPILATION_TARGETS: (
        SetCompilationTargetsRequest,
        None,
        SetCompilationTargetsParams,
        None,
    ),
    # Notification
    ANALYSIS_REPORT_ANALYSIS_PROGRESS: (
        ReportAnalysisProgressNotification,
        None,
        AnalysisProgressParams,
        None,
    ),
}
