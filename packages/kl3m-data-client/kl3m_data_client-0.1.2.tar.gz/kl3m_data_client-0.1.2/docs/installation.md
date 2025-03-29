# Installation Guide

The KL3M Data Client can be installed in several ways depending on your needs.

## Standard Installation

For regular usage as a Python library, install from PyPI:

```bash
pip install kl3m-data-client
```

## Development Installation

For development purposes, install with additional development dependencies:

```bash
# Clone the repository
git clone https://github.com/alea-institute/kl3m-data-client.git
cd kl3m-data-client/

# Install in development mode with dev extras
pip install -e ".[dev]"
```

## CLI Installation with pipx

For a globally available command-line tool that doesn't interfere with your Python environment:

```bash
pipx install kl3m-data-client
```

This installs the `kl3m-client` command in your PATH.

## Requirements

The KL3M Data Client requires:

- Python 3.9 or higher
- boto3 for AWS S3 interaction
- pyarrow for parquet file processing
- rich for enhanced console output
- tokenizers for token counting and decode/encode

All dependencies are automatically installed when you install the package.