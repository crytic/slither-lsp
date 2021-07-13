import os
from typing import Iterable, Set
from urllib.parse import unquote_plus, urlparse, urljoin
from urllib.request import url2pathname, pathname2url


def is_solidity_file(path: str) -> bool:
    filename_base, file_extension = os.path.splitext(path)
    return file_extension is not None and file_extension.lower() == '.sol'


def uri_to_fs_path(uri: str) -> str:
    path = url2pathname(unquote_plus(urlparse(uri).path))
    return path


def fs_path_to_uri(path: str) -> str:
    uri = urljoin('file:', pathname2url(path))
    return uri


def get_solidity_files(folders: Iterable[str], recursive=True) -> Set[str]:
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
        for item in os.listdir(folder):
            full_path = os.path.join(folder, item)
            if os.path.isfile(full_path):
                if is_solidity_file(full_path):
                    solidity_files.add(full_path)
            elif recursive and os.path.isdir(full_path):
                # If recursive, join our set with any other discovered files in subdirectories.
                if item != 'node_modules':
                    solidity_files.update(
                        get_solidity_files([full_path], recursive)
                    )

    # Return all discovered solidity files
    return solidity_files
