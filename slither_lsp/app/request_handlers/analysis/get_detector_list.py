from typing import Any

from pygls.server import LanguageServer
from slither.__main__ import get_detectors_and_printers, output_detectors_json


def get_detector_list(ls: LanguageServer, params: Any) -> Any:
    """
    Handler which invokes slither to obtain a list of all detectors and some properties that describe them.
    """

    # Obtain a list of detectors
    detectors, _ = get_detectors_and_printers()

    # Obtain the relevant object to be output as JSON.
    detector_types_json = output_detectors_json(detectors)
    return detector_types_json
