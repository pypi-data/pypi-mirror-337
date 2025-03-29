# KL3MClient

The `KL3MClient` class is the primary interface for interacting with KL3M data.

## Class Definition

```python
class KL3MClient:
    def __init__(
        self,
        bucket_name: str = "data.kl3m.ai",
        region: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        verbose: bool = False
    ) -> None:
        """
        Initialize a KL3M data client.
        
        Args:
            bucket_name: S3 bucket name containing KL3M data
            region: AWS region (optional, uses environment variable if not provided)
            aws_access_key_id: AWS access key (optional)
            aws_secret_access_key: AWS secret key (optional)
            verbose: Enable verbose logging
        """
```

## Methods

### Dataset Operations

```python
def list_datasets(self) -> List[str]:
    """
    List all available datasets.
    
    Returns:
        List of dataset IDs
    """
    
def get_dataset_status(self, dataset_id: str) -> DatasetStatus:
    """
    Get the status of a dataset.
    
    Args:
        dataset_id: The dataset identifier
        
    Returns:
        DatasetStatus object containing information about the dataset
    """

def iter_documents(
    self, 
    dataset_id: str, 
    stage: Stage, 
    limit: Optional[int] = None
) -> Iterator[str]:
    """
    Iterator over document IDs in a dataset.
    
    Args:
        dataset_id: Dataset identifier
        stage: Pipeline stage to use
        limit: Maximum number of documents to yield
        
    Returns:
        Iterator yielding document IDs
    """
```

### Document Operations

```python
def get_document(
    self, 
    dataset_id: str, 
    document_id: str, 
    stage: Stage = Stage.DOCUMENTS
) -> Optional[Document]:
    """
    Get a document from a dataset.
    
    Args:
        dataset_id: Dataset identifier
        document_id: Document identifier
        stage: Pipeline stage to use
        
    Returns:
        Document object or None if not found
    """

def get_documents(
    self, 
    dataset_id: str, 
    document_ids: List[str], 
    stage: Stage = Stage.DOCUMENTS
) -> Dict[str, Optional[Document]]:
    """
    Get multiple documents by ID.
    
    Args:
        dataset_id: Dataset identifier
        document_ids: List of document identifiers
        stage: Pipeline stage to use
        
    Returns:
        Dictionary mapping document IDs to Document objects
    """
```

### Export Operations

```python
def export_to_jsonl(
    self,
    dataset_id: str,
    output_path: str,
    source_stage: Stage = Stage.PARQUET,
    max_documents: Optional[int] = None,
    deduplicate: bool = True,
    compress: bool = False,
    exclude_content: bool = False,
    verbose: bool = False
) -> None:
    """
    Export a dataset to JSONL format.
    
    Args:
        dataset_id: Dataset identifier
        output_path: Path to output JSONL file
        source_stage: Stage to export from
        max_documents: Maximum documents to export
        deduplicate: Deduplicate documents by ID
        compress: Compress output with gzip
        exclude_content: Exclude document content
        verbose: Show progress information
    """

def iter_jsonl_export(
    self,
    dataset_id: str,
    source_stage: Stage = Stage.PARQUET,
    max_documents: Optional[int] = None,
    deduplicate: bool = True,
    exclude_content: bool = False
) -> Iterator[Dict[str, Any]]:
    """
    Iterate over documents for export.
    
    Args:
        dataset_id: Dataset identifier
        source_stage: Stage to export from
        max_documents: Maximum documents to export
        deduplicate: Deduplicate documents by ID
        exclude_content: Exclude document content
        
    Returns:
        Iterator yielding document dictionaries
    """
```

## Examples

```python
# Initialize client
client = KL3MClient()

# List datasets
datasets = client.list_datasets()
print(f"Available datasets: {datasets}")

# Get dataset status
status = client.get_dataset_status("usc")
print(f"USC dataset has {status.document_count} documents")

# Get a document
document = client.get_document("usc", "12345")
content = document.get_content(Stage.DOCUMENTS)
print(f"Document title: {content.metadata.title}")

# Export to JSONL
client.export_to_jsonl(
    dataset_id="usc",
    output_path="usc_export.jsonl",
    max_documents=1000
)
```