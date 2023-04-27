# Slither Language Server Protocol

## Development Installation

- Create a new python virtual environment

```bash
python3 -m venv /path/to/new/virtual/env/slither-lsp-env
source /path/to/new/virtual/env/slither-lsp-env/bin/activate
```

- Clone and install slither-lsp locally

```bash
git clone git@github.com:crytic/slither-lsp.git
cd slither-lsp
git checkout dev
pip3 install -e .
cd ..
```

- Clone and install slither-vscode locally

```bash
git clone git@github.com:crytic/slither-vscode.git
cd slither-vscode
git checkout dev
npm install
```

- Open slither-vscode folder in VSCode

```bash
cd /path/to/slither-vscode
code .
```

- Press `f5` to start slither-vscode extension in debugger mode
- Open a Solidity project in VSCode and test
