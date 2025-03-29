# KL3M Data Client

A lightweight client for interacting with the KL3M data pipeline and S3 storage architecture.

## Features

- Access and manage KL3M datasets stored in S3
- List datasets and check their processing status
- Retrieve and parse document content from all pipeline stages
- Both programmatic and command-line interfaces with JSON output support
- Minimal dependencies (boto3, pyarrow, rich, and tokenizers)
- Streaming support for efficient handling of large datasets

## Installation

```bash
pip install kl3m-data-client
```

For development:

```bash
pip install -e ".[dev]"
```

Or using pipx for a globally available CLI tool:

```bash
pipx install kl3m-data-client
```

## Developer API Usage

### Basic Usage

```python
from kl3m_data_client import KL3MClient
from kl3m_data_client.models.common import Stage

# Initialize client
client = KL3MClient()

# List available datasets
datasets = client.list_datasets()

# Get status of a specific dataset
status = client.get_dataset_status("usc")
print(f"Dataset: {status.dataset_id}")
print(f"Document count: {status.document_count}")
print(f"Is complete: {status.is_complete}")
print(f"Missing representations: {status.missing_representations}")
print(f"Missing parquet: {status.missing_parquet}")

# Streaming document IDs with a limit (efficient for large datasets)
for doc_id in client.iter_documents("fdlp", Stage.DOCUMENTS, limit=5):
    # Process each document as it's retrieved
    document = client.get_document("fdlp", doc_id, Stage.DOCUMENTS)
    content = document.get_content(Stage.DOCUMENTS)
    
    # Print basic metadata
    print(f"Document: {doc_id}, Title: {content.metadata.title}")
    
    # Check if content is binary (e.g., PDF) or text
    if isinstance(content.content, bytes):
        # Handle binary content
        content_size = len(content.content)
        print(f"Binary content ({content_size} bytes), Format: {content.metadata.format}")
        
        # Save binary content to a file if needed
        # with open(f"{doc_id}.bin", "wb") as f:
        #     f.write(content.content)
    else:
        # Handle text content
        print(f"Text content preview: {content.content[:100]}...")
    
    # No need to load the entire dataset into memory!

# You can perform custom processing on each document
# without loading the entire dataset into memory
for doc_id in client.iter_documents("usc", Stage.PARQUET, limit=100):
    document = client.get_document("usc", doc_id, Stage.PARQUET)
    parquet = document.get_parquet()
    if parquet:
        reps = parquet.get_representations()
        for rep_type, tokens in reps.items():
            print(f"Document: {doc_id}, Type: {rep_type}, Tokens: {len(tokens)}")
```

See the `examples` directory for more detailed usage examples.

### Working with Documents and Representations

The library provides dedicated classes for easily working with document data across all stages:

```python
from kl3m_data_client import KL3MClient
from kl3m_data_client.models.common import Stage

# Initialize client
client = KL3MClient()

# Get a document
document = client.get_document("cap", "1000")

# === Document Stage ===
# Get basic document content
doc_content = document.get_content(Stage.DOCUMENTS)
print(f"Title: {doc_content.metadata.title}")

# Title: Phyllis MERRIWEATHER, Plaintiff-Appellee, v. FAMILY DOLLAR STORES OF INDIANA, INC. Defendant-Appellant

# Handle both text and binary content
if isinstance(doc_content.content, bytes):
    # Binary content (PDFs, images, etc.)
    print(f"Binary content ({len(doc_content.content)} bytes)")
    print(f"Format: {doc_content.metadata.format}")
    # Save binary content if needed
    # with open("document.bin", "wb") as f:
    #     f.write(doc_content.content)
else:
    # Text content
    print(f"Content preview: {doc_content.content[:100]}...")
    
# Content preview: <!DOCTYPE html>
# <html>
# <body>
# <section class="casebody" data-case-id="32044032500381_0085" data-firs...

# === Representation Stage ===
# Get representation using the convenient helper method
representation = document.get_representation()

# Access representation data with a clean API
available_mime_types = representation.get_available_mime_types()
print(f"Available MIME types: {available_mime_types}")

# Available MIME types: ['text/markdown']

# Get content for a specific MIME type
content = representation.get_content("text/markdown")
print(content[0:100] + "...")

# #### Phyllis MERRIWEATHER, Plaintiff-Appellee, v. FAMILY DOLLAR STORES OF INDIANA, INC. Defendant-Ap...

# Get a summary of all representations
summary = representation.summarize()
print(summary)

# {'document_id': 's3://data.kl3m.ai/documents/cap/1000.json', 'source': 'https://static.case.law/', 'mime_types': ['text/markdown'], 'token_counts': {'text/markdown': {'alea-institute/kl3m-003-64k': 6245}}}

# === Parquet Stage ===
# Get parquet data with PyArrow support
parquet = document.get_parquet()
print(f"Parquet size: {parquet.size} bytes")

# Parquet size: 12205 bytes

# Get PyArrow table
table = parquet.get_table()
print(f"Table columns: {parquet.get_columns()}")
print(f"Schema: {parquet.get_schema()}")

# Table columns: ['identifier', 'representations']
# Schema: identifier: string
# representations: map<string, list<element: uint32> ('representations')>
#   child 0, representations: struct<key: string not null, value: list<element: uint32>> not null
#       child 0, key: string not null
#       child 1, value: list<element: uint32>
#           child 0, element: uint32

# Access document representations from parquet
representations = parquet.get_representations()
for rep_type, tokens in representations.items():
    print(f"{rep_type}: {len(tokens)} tokens")

# text/markdown: 5834 tokens
```

### Low-level S3 Utilities

The library also exposes low-level S3 utilities for advanced usage:

```python
from kl3m_data_client.utils.s3 import (
    get_s3_client,
    list_dataset_ids,
    get_stage_prefix,
    iter_prefix,
    check_object_exists,
    get_object_bytes,
    decompress_content,
)

# Initialize S3 client directly
s3_client = get_s3_client()

# List datasets directly using S3 utilities
datasets = list_dataset_ids(s3_client, "data.kl3m.ai", Stage.DOCUMENTS)

# Iterate through S3 keys (streaming)
for key in iter_prefix(s3_client, "data.kl3m.ai", "documents/usc/"):
    # Process each key as it comes in
    pass
```

## Command Line Interface

```bash
# List all datasets
kl3m-client list

# Show status of a dataset
kl3m-client status usc

# List documents in a dataset
kl3m-client documents usc --stage documents --count

# Inspect a specific document
kl3m-client inspect usc document_id --stage documents

# JSON output is supported for all commands
kl3m-client status usc --json
```

For detailed CLI documentation:

```bash
kl3m-client --help
kl3m-client <command> --help
```

See the [CLI Reference](docs/cli-reference.md) for complete documentation including JSON output examples.

## AWS Authentication

The client uses boto3 for S3 access and supports all standard AWS authentication methods:

1. Environment variables (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`)
2. Shared credential file (`~/.aws/credentials`)
3. AWS config file (`~/.aws/config`)
4. IAM role for Amazon EC2

You can also explicitly provide credentials when initializing the client:

```python
client = KL3MClient(
    aws_access_key_id="YOUR_ACCESS_KEY",
    aws_secret_access_key="YOUR_SECRET_KEY", 
    region="us-east-1"
)
```

## Repository

- Source Code: [https://github.com/alea-institute/kl3m-data-client](https://github.com/alea-institute/kl3m-data-client)
- Bug Tracker: [https://github.com/alea-institute/kl3m-data-client/issues](https://github.com/alea-institute/kl3m-data-client/issues)
- Documentation: [https://github.com/alea-institute/kl3m-data-client/tree/main/docs](https://github.com/alea-institute/kl3m-data-client/tree/main/docs)

## License

MIT