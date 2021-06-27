from setuptools import setup, find_packages

setup(
    name="slither-lsp",
    description="Language Server powered by the Slither static analyzer",
    url="https://github.com/crytic/slither-lsp",
    author="Trail of Bits",
    version="0.0.1",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "slither-analyzer>=0.8.0",
        "pymitter>=0.3.1"
    ],
    dependency_links=[],
    license="AGPL-3.0",
    long_description=open("README.md").read(),
    entry_points={
        "console_scripts": [
            "slither-lsp = slither_lsp.__main__:main",
        ]
    },
)
