"""
KL3M Data Client

A lightweight client for interacting with KL3M datasets stored in S3.

The client provides a simple interface for:
- Listing available datasets
- Retrieving dataset status and counts
- Accessing document content from various pipeline stages
- Exporting datasets to JSONL format

Basic Usage:
```python
from kl3m_data_client import KL3MClient
from kl3m_data_client.models.common import Stage

# Initialize client
client = KL3MClient()

# List datasets
datasets = client.list_datasets()

# Get dataset status
status = client.get_dataset_status("usc")

# Get a document
document = client.get_document("usc", "document_id", Stage.DOCUMENTS)
content = document.get_content(Stage.DOCUMENTS)

# Export to JSONL
client.export_to_jsonl("usc", "output.jsonl")
```

For more examples, see the 'examples' directory.
"""

from kl3m_data_client.client import KL3MClient
from kl3m_data_client.document import Document
from kl3m_data_client.models.common import Stage

__version__ = "0.1.2"

__all__ = ["KL3MClient", "Document", "Stage"]
