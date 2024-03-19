from typing import List, Optional

import attrs
from slither_lsp.app.types.analysis_structures import CompilationTarget


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
