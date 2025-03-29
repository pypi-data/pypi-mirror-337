# KL3M Data Client

A lightweight client for interacting with the KL3M data pipeline and S3 storage architecture.

## Features

- Access and manage KL3M datasets stored in S3
- List datasets and check their processing status
- Retrieve and parse document content from all pipeline stages
- Export datasets to JSONL format with filtering options
- Both programmatic and command-line interfaces
- Minimal dependencies (only boto3 and rich)
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

# Streaming document IDs with a limit (efficient for large datasets)
for doc_id in client.iter_documents("usc", Stage.DOCUMENTS, limit=5):
    # Process each document as it's retrieved
    document = client.get_document("usc", doc_id, Stage.DOCUMENTS)
    content = document.get_content(Stage.DOCUMENTS)
    print(f"Document: {doc_id}, Title: {content.metadata.title}")
    
    # No need to load the entire dataset into memory!

# Export to JSONL using streaming
client.export_to_jsonl(
    dataset_id="usc",
    output_path="usc_export.jsonl",
    source_stage=Stage.PARQUET,
    max_documents=1000,
    deduplicate=True,
)

# Process documents during export with streaming iterator
for document in client.iter_jsonl_export(
    dataset_id="usc",
    source_stage=Stage.PARQUET,
    max_documents=100,
    deduplicate=True,
):
    # Process each document as it's streamed
    print(f"Document: {document['id']}")
    print(f"Token count: {len(document['tokens'])}")
    
    # You can perform custom processing on each document here
    # without loading the entire dataset into memory
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
print(f"Content preview: {doc_content.content[:100]}...")

# === Representation Stage ===
# Get representation using the convenient helper method
representation = document.get_representation()

# Access representation data with a clean API
available_mime_types = representation.get_available_mime_types()
print(f"Available MIME types: {available_mime_types}")

# Get content for a specific MIME type
markdown_content = representation.get_content("text/markdown")

# Get available tokenizers for a representation
tokenizers = representation.get_available_tokenizers("text/markdown")
print(f"Available tokenizers: {tokenizers}")

# Get tokens and token count
tokens = representation.get_tokens("text/markdown", "cl100k_base")
token_count = representation.token_count("text/markdown", "cl100k_base")
print(f"Token count: {token_count}")

# Get a summary of all representations
summary = representation.summarize()
print(summary)

# === Parquet Stage ===
# Get parquet data with PyArrow support
parquet = document.get_parquet()
print(f"Parquet size: {parquet.size} bytes")

# Get PyArrow table
table = parquet.get_table()
print(f"Table columns: {parquet.get_columns()}")
print(f"Schema: {parquet.get_schema()}")

# Access document representations from parquet
representations = parquet.get_representations()
for rep_type, tokens in representations.items():
    print(f"{rep_type}: {len(tokens)} tokens")

# Save parquet data to a file
parquet.save_to_file("document.parquet")
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

# Export a dataset to JSONL
kl3m-client export-jsonl usc --output usc_export.jsonl
```

For detailed CLI documentation:

```bash
kl3m-client --help
kl3m-client <command> --help
```

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

## License

MIT