from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Set

import lsprotocol.types as lsp
from slither_lsp.app.types.analysis_structures import (
    AnalysisResult,
    SlitherDetectorSettings,
)
from slither_lsp.app.utils.file_paths import fs_path_to_uri

if TYPE_CHECKING:
    from slither_lsp.app.slither_server import SlitherServer


class SlitherDiagnostics:
    """
    Tracks and reports diagnostics that were derived from AnalysisResults
    """

    def __init__(self, context: SlitherServer):
        # Set basic parameters
        self.context = context

        # Define a lookup of file uri -> diagnostics. This is necessary so we can track non-existent diagnostics.
        self.diagnostics: Dict[str, lsp.PublishDiagnosticsParams] = {}

        # TODO: Detector filters

    def update(
        self,
        analysis_results: List[AnalysisResult],
        detector_settings: SlitherDetectorSettings,
    ) -> None:
        """
        Generates and tracks the diagnostics for provided analysis results and detector settings.
        :param analysis_results: Analysis results containing detector results which diagnostics will be generated from.
        :param detector_settings: User-provided settings for slither detector results.
        :return: None
        """
        # Create a new diagnostics array which our current array will be swapped to later.
        new_diagnostics: Dict[str, lsp.PublishDiagnosticsParams] = {}

        # Convert our hidden checks to a set
        hidden_checks = set(detector_settings.hidden_checks)

        # Compile our list of diagnostics for all analyses and all their underlying detector finders.
        if detector_settings.enabled:
            for analysis_result in analysis_results:
                # Skip any analyses without detector results
                if analysis_result.detector_results is None:
                    continue

                for detector_result in analysis_result.detector_results:
                    # If we don't have any source mappings, skip this.
                    if (
                        len(detector_result.elements) == 0
                        or detector_result.elements[0].source_mapping is None
                    ):
                        continue

                    # If our result is for a check we're skipping, do so.
                    if detector_result.check in hidden_checks:
                        continue

                    # Obtain the target filename for this finding (the first element is the most significant)
                    target_result_element = detector_result.elements[0]
                    target_uri = fs_path_to_uri(
                        target_result_element.source_mapping.filename_absolute
                    )

                    # Obtain our params for this file uri, or create them if they haven't been yet.
                    params = new_diagnostics.get(target_uri, None)
                    if params is None:
                        params = lsp.PublishDiagnosticsParams(
                            uri=target_uri, version=None, diagnostics=[]
                        )
                        new_diagnostics[target_uri] = params

                    # Add our detector result as a diagnostic.
                    params.diagnostics.append(
                        lsp.Diagnostic(
                            lsp.Range(
                                start=lsp.Position(
                                    line=target_result_element.source_mapping.lines[0]
                                    - 1,
                                    character=target_result_element.source_mapping.starting_column
                                    - 1,
                                ),
                                end=lsp.Position(
                                    line=target_result_element.source_mapping.lines[-1]
                                    - 1,
                                    character=target_result_element.source_mapping.ending_column
                                    - 1,
                                ),
                            ),
                            message=f"[{detector_result.impact.upper()}] {detector_result.description}",
                            severity=lsp.DiagnosticSeverity.Information,
                            code=detector_result.check,
                            source="slither",
                        )
                    )

        # Clear any diagnostics for files that no longer have any.
        files_to_clear: Set[str] = set(self.diagnostics) - set(new_diagnostics)
        for file_to_clear in files_to_clear:
            self._clear_single(file_to_clear, False)

        # Set our diagnostics as the new array
        self.diagnostics = new_diagnostics

        # Loop for each diagnostic and broadcast all of them.
        for diagnostic_params in self.diagnostics.values():
            self.context.publish_diagnostics(
                diagnostic_params.uri, diagnostics=diagnostic_params.diagnostics
            )

    def _clear_single(self, file_uri: str, clear_from_lookup: bool = False) -> None:
        """
        Clears a single file's diagnostics, and optionally removes it from the lookup maintained by this object.
        :param file_uri: The uri of the file to clear diagnostics for.
        :param clear_from_lookup: Indicates whether the lookup tracking file diagnostics should be purged of this
        diagnostic.
        :return: None
        """
        # Send empty diagnostics for this file to the client.
        self.context.publish_diagnostics(file_uri, [])

        # Optionally clear this item from the diagnostic lookup
        if clear_from_lookup:
            self.diagnostics.pop(file_uri, None)

    def clear(self) -> None:
        """
        Clears all previously published diagnostics by this object.
        :return: None
        """
        # Loop through all diagnostic files, publish new diagnostics for each file with no items.
        for file_uri in self.diagnostics.keys():
            self._clear_single(file_uri, False)

        # Clear the dictionary
        self.diagnostics.clear()
