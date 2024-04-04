# Slither Language Server

## How to install

Run the following command from the project root directory (preferably inside a Python virtual environment):

    python -m pip install .

## Features

* Go to implementations/definitions
* Find all references
* Show call hierarchy
* Show type hierarchy
* View and filter detector results

## Adding new features

New request handlers should be registered in the [constructor of `SlitherServer`](https://github.com/crytic/slither-lsp/blob/4e951da5244b15b69a5cbf4ce2444f205a0d0417/slither_lsp/app/slither_server.py#L120). Please note that in order to keep the conceptual load to a minimum, handlers should not be declared directly in the `SlitherServer` class itself. Instead, related handlers should be declared in a separate module. See [`goto_def_impl_refs.py`](https://github.com/crytic/slither-lsp/blob/c914576b74f748f69738a0a7a38ee6d53bfd1614/slither_lsp/app/request_handlers/goto_def_impl_refs.py) as an example.

The Slither Language Server uses [`pygls`](https://pygls.readthedocs.io/en/latest/index.html) as the LSP implementation, and you should refer to its documentation when writing new handlers.

If you're adding an handler for a standard LSP feature, there will be no need to do anything on the VSCode extension side: VSCode will automatically hook its commands to use the provided feature.

If, on the other hand, the feature you're trying to add does not map to a standard LSP feature, you will need to register a custom handler. See [`$/slither/analyze`](https://github.com/crytic/slither-lsp/blob/4e951da5244b15b69a5cbf4ce2444f205a0d0417/slither_lsp/app/slither_server.py#L117) as an example: note how each request name is prefixed with `$/slither/`. You will need to manually send request from the VSCode extension in order to trigger these handlers.
