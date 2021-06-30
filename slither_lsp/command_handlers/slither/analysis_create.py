import os
from enum import Enum
from typing import Any

from crytic_compile import CryticCompile
from crytic_compile.platform.solc_standard_json import SolcStandardJson
from slither import Slither

from slither_lsp.command_handlers.base_handler import BaseCommandHandler
from slither_lsp.types.lsp_errors import LSPError, LSPErrorCode
from slither_lsp.state.server_context import ServerContext


class CompilationSettingsTargetType(Enum):
    """
    Defines the possible options for target types in provided compilation settings.
    """
    BASIC = 'basic'
    STANDARD_JSON = 'solc_standard_json'


class AnalysisCreateHandler(BaseCommandHandler):
    """
    Handler which invokes slither analysis on a given target and returns an analysis identifier
    which can be used to perform subsequent operations on.
    """
    method_name = "$/slither/analysis/create"

    @classmethod
    def process(cls, context: ServerContext, params: Any) -> Any:
        # Verify we were provided compilation settings
        if 'compilationSettings' not in params:
            raise LSPError(
                LSPErrorCode.InvalidParams,
                "'compilation_settings' key was not provided for analysis.",
                None
            )

        # Obtain our optional cwd
        cwd = os.getcwd()
        if 'cwd' in params:
            cwd = params['cwd']

        # Obtain our compilation settings
        compilation_settings = params['compilationSettings']

        # Verify we were provided a type
        if 'type' not in compilation_settings:
            raise LSPError(
                LSPErrorCode.InvalidParams,
                "'type' key was not provided for compilation settings'",
                None
            )

        # Obtain our compilation type
        target_type: CompilationSettingsTargetType = CompilationSettingsTargetType(compilation_settings['type'])

        # If this is a basic analysis, we simply use a target and pass some other parameters
        # Otherwise, we construct a solc standard JSON
        if target_type is CompilationSettingsTargetType.BASIC:
            # Verify we have a target
            if 'basic' not in compilation_settings or 'target' not in compilation_settings['basic']:
                raise LSPError(
                    LSPErrorCode.InvalidParams,
                    "Compilation target type is basic, but 'basic->target' was not provided",
                    None
                )

            # Perform analysis on our target
            # TODO: Pass other parameters (remappings and possibly other arbitrary ones).
            slither = Slither(compilation_settings['basic']['target'], solc_working_dir=cwd)
        elif target_type is CompilationSettingsTargetType.STANDARD_JSON:
            # We're compiling with solc standard JSON. The compilation settings is the JSON itself.
            standard_json = SolcStandardJson(compilation_settings[target_type.value])
            compilation = CryticCompile(standard_json, solc_working_dir=cwd)
            slither = Slither(compilation)
        else:
            raise LSPError(
                LSPErrorCode.InvalidParams,
                f"'{target_type}' is not a supported compilation type.",
                None
            )

        # Register the analysis and obtain an id for it.
        analysis_id = context.register_analysis(slither)

        # Return the analysis id
        return {
            'analysisId': analysis_id
        }
