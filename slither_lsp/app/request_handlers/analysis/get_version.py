from importlib.metadata import version as pkg_version
from typing import Any

from pygls.server import LanguageServer


def get_version(ls: LanguageServer, params: Any) -> Any:
    """
    Handler which retrieves versions for slither, crytic-compile, and related applications.
    """

    return {
        "slither": pkg_version("slither-analyzer"),
        "crytic_compile": pkg_version("crytic-compile"),
        "slither_lsp": pkg_version("slither-lsp"),
    }
