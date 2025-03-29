# Getting Started

This guide will help you get started with the KL3M Data Client library.

## Basic Setup

First, import the necessary modules:

```python
from kl3m_data_client import KL3MClient
from kl3m_data_client.models.common import Stage
```

Initialize the client:

```python
# Basic initialization (uses environment variables for AWS credentials)
client = KL3MClient()

# With explicit AWS credentials
client = KL3MClient(
    aws_access_key_id="YOUR_ACCESS_KEY",
    aws_secret_access_key="YOUR_SECRET_KEY",
    region="us-east-1",
    verbose=True  # Enable verbose logging
)
```

## List Available Datasets

To see what datasets are available:

```python
datasets = client.list_datasets()
for dataset in datasets:
    print(dataset)
```

## Get Dataset Status

Check the processing status and document count for a dataset:

```python
status = client.get_dataset_status("usc")
print(f"Dataset: {status.dataset_id}")
print(f"Document count: {status.document_count}")
print(f"Status: {status.processing_status}")
```

## Working with Documents

Retrieve and process documents from a dataset:

```python
# Get a single document
document = client.get_document("usc", "document_id")

# Get its content
content = document.get_content(Stage.DOCUMENTS)
print(f"Title: {content.metadata.title}")
print(f"Content: {content.content[:100]}...")

# Get document representation
rep = document.get_representation()
mime_types = rep.get_available_mime_types()
print(f"Available MIME types: {mime_types}")

# Get tokens for a representation
tokenizers = rep.get_available_tokenizers(mime_types[0])
tokens = rep.get_tokens(mime_types[0], tokenizers[0])
print(f"Token count: {len(tokens)}")
```

## Streaming Documents

For large datasets, use streaming iterators:

```python
# Stream document IDs
for doc_id in client.iter_documents("usc", Stage.DOCUMENTS, limit=10):
    # Process each document ID as needed
    document = client.get_document("usc", doc_id, Stage.DOCUMENTS)
    # ...process document...
    
# Stream document export
for doc in client.iter_jsonl_export("usc", Stage.PARQUET, max_documents=100):
    # Process each exported document dictionary
    print(f"Document ID: {doc['id']}")
```

## Exporting Data

Export a dataset to JSONL:

```python
client.export_to_jsonl(
    dataset_id="usc",
    output_path="usc_export.jsonl",
    source_stage=Stage.PARQUET,
    max_documents=1000,
    deduplicate=True
)
```

## Next Steps

- Check the [API Reference](api-reference/index.md) for detailed information on all classes and methods.
- Explore [CLI Reference](cli-reference.md) for command-line usage.
- See [Advanced Usage](advanced-usage.md) for more complex examples.