from typing import List, Optional, Union

import attrs
from slither_lsp.app.types.analysis_structures import SlitherDetectorSettings


@attrs.define
class AnalysisRequestParams:
    uris: Optional[List[str]] = attrs.field()


SLITHER_ANALYZE = "$/slither/analyze"
SLITHER_GET_DETECTOR_LIST = "$/slither/getDetectorList"
SLITHER_GET_VERSION = "$/slither/getVersion"
SLITHER_SET_DETECTOR_SETTINGS = "$/slither/setDetectorSettings"
CRYTIC_COMPILE_GET_COMMAND_LINE_ARGUMENTS = "$/cryticCompile/getCommandLineArguments"


@attrs.define
class SetDetectorSettingsRequest:
    id: Union[int, str] = attrs.field()
    params: SlitherDetectorSettings = attrs.field()
    method: str = SLITHER_SET_DETECTOR_SETTINGS
    jsonrpc: str = attrs.field(default="2.0")


METHOD_TO_TYPES = {
    # Requests
    SLITHER_SET_DETECTOR_SETTINGS: (
        SetDetectorSettingsRequest,
        None,
        SlitherDetectorSettings,
        None,
    ),
}
