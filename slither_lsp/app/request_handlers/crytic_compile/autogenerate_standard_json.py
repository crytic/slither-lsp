import os
from typing import Any, Iterable, Set

from crytic_compile.platform.solc_standard_json import SolcStandardJson

from slither_lsp.lsp.request_handlers.base_handler import BaseRequestHandler
from slither_lsp.lsp.state.server_context import ServerContext


def get_solidity_files(folders: Iterable[str], recursive=True) -> Set:
    """
    Loops through all provided folders and obtains a list of all solidity files existing in them.
    This skips 'node_module' folders created by npm/yarn.
    :param folders: A list of folders to search for Solidity files within.
    :param recursive: Indicates if the search for Solidity files should be recursive.
    :return: A list of Solidity file paths which were discovered in the provided folders.
    """
    # Create our resulting set
    solidity_files = set()
    for folder in folders:
        for root, dirs, files in os.walk(folder):
            # Loop through all files and determine if any have a .sol extension
            for file in files:
                filename_base, file_extension = os.path.splitext(file)
                if file_extension is not None and file_extension.lower() == '.sol':
                    solidity_files.add(os.path.join(root, file))

            # If recursive, join our set with any other discovered files in subdirectories.
            if recursive:
                solidity_files.update(
                    get_solidity_files([os.path.join(root, d) for d in dirs], recursive)
                )

    # Return all discovered solidity files
    return solidity_files


class AutogenerateStandardJsonHandler(BaseRequestHandler):
    """
    Handler which auto-generates solc standard JSON manifests for Solidity files under a given
    directory.
    """
    method_name = "$/cryticCompile/solcStandardJson/autogenerate"

    @staticmethod
    def process(context: ServerContext, params: Any) -> Any:

        # Obtain our target files and folders.
        files = set()
        folders = set()
        if 'files' in params and isinstance(params['files'], list):
            files.update(params['files'])
        if 'folders' in params and isinstance(params['folders'], list):
            folders.update(params['folders'])

        # Get a list of all solidity files in our folders
        files.update(get_solidity_files(folders))

        # TODO: Parse import strings, create remappings for unresolved imports.
        # Regex: import\s+[^"]*"([^"]+)".*;

        # TODO: Parse semvers, find incompatibilities, put them into different compilation buckets
        #  and potentially return data about satisfactory solc versions, which may enable us to
        #  use solc-select to compile all.
        # Regex: pragma\s+solidity\s+(.*);

        # TODO: For now we return a single json manifest, but we want to split them if we have
        #  version conflicts.
        standard_json = SolcStandardJson()
        for file in files:
            standard_json.add_source_file(file)

        return [
            standard_json.to_dict()
        ]
