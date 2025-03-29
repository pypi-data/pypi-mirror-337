# KL3M Data Client Documentation

Welcome to the KL3M Data Client documentation. This library provides tools to interact with the KL3M data pipeline and S3 storage architecture.

## Table of Contents

1. [Installation Guide](installation.md)
2. [Getting Started](getting-started.md)
3. [API Reference](api-reference/index.md)
4. [CLI Reference](cli-reference.md)
5. [Advanced Usage](advanced-usage.md)
6. [AWS Integration](aws-integration.md)

## Overview

The KL3M Data Client is designed to provide easy access to KL3M datasets stored in S3. It offers both a programmatic interface and a command-line tool, allowing you to:

- List available datasets
- Retrieve dataset status information
- Access and process documents from all pipeline stages
- Export datasets to JSONL with filtering capabilities
- Stream data efficiently without loading entire datasets into memory

## Key Features

- **Streaming Processing**: Efficiently handle large datasets with streaming iterators
- **Multi-stage Access**: Access data from all KL3M pipeline stages (documents, representations, parquet)
- **S3 Integration**: Built-in support for AWS S3 with authentication flexibility
- **Command-line Interface**: Complete CLI with helpful commands and rich output
- **Document Processing**: Tools for inspecting and working with document content and metadata

Check out the [Getting Started](getting-started.md) guide for a quick introduction to using the library.