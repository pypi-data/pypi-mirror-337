# Advanced Usage

This guide covers advanced usage patterns for the KL3M Data Client library.

## Working with Multiple Datasets

```python
from kl3m_data_client import KL3MClient
from kl3m_data_client.models.common import Stage
from concurrent.futures import ThreadPoolExecutor

client = KL3MClient()

# Get status of multiple datasets in parallel
datasets = ["usc", "cap", "fdlp"]

def get_status(dataset_id):
    status = client.get_dataset_status(dataset_id)
    return {
        "dataset_id": status.dataset_id,
        "document_count": status.document_count,
        "processing_status": status.processing_status
    }

with ThreadPoolExecutor(max_workers=len(datasets)) as executor:
    results = list(executor.map(get_status, datasets))

for result in results:
    print(f"{result['dataset_id']}: {result['document_count']} documents")
```

## Custom Document Processing

```python
from kl3m_data_client import KL3MClient
from kl3m_data_client.models.common import Stage
import json

client = KL3MClient()

# Define a custom document processor
def process_document(doc_data):
    # Extract section titles with regex
    import re
    content = doc_data.get("content", "")
    sections = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
    
    return {
        "id": doc_data["id"],
        "title": doc_data.get("metadata", {}).get("title", ""),
        "section_count": len(sections),
        "sections": sections[:10]  # First 10 sections only
    }

# Process documents during export
processed_docs = []

for doc in client.iter_jsonl_export(
    dataset_id="cap",
    source_stage=Stage.DOCUMENTS,
    max_documents=50
):
    processed_doc = process_document(doc)
    processed_docs.append(processed_doc)

# Save processed results
with open("processed_documents.json", "w") as f:
    json.dump(processed_docs, f, indent=2)
```

## Working with Document Representations

```python
from kl3m_data_client import KL3MClient
from kl3m_data_client.models.common import Stage
import statistics

client = KL3MClient()

# Analyze token counts across documents
token_counts = []
tokenizer = "cl100k_base"
mime_type = "text/markdown"

for doc_id in client.iter_documents("usc", Stage.REPRESENTATIONS, limit=100):
    document = client.get_document("usc", doc_id, Stage.REPRESENTATIONS)
    representation = document.get_representation()
    
    if representation and mime_type in representation.get_available_mime_types():
        if tokenizer in representation.get_available_tokenizers(mime_type):
            count = representation.token_count(mime_type, tokenizer)
            token_counts.append(count)
            
# Calculate statistics
if token_counts:
    print(f"Token count statistics for {len(token_counts)} documents:")
    print(f"  Average: {statistics.mean(token_counts):.1f}")
    print(f"  Median: {statistics.median(token_counts)}")
    print(f"  Min: {min(token_counts)}")
    print(f"  Max: {max(token_counts)}")
    print(f"  Std Dev: {statistics.stdev(token_counts):.1f}")
```

## Custom Parquet Operations

```python
from kl3m_data_client import KL3MClient
from kl3m_data_client.models.common import Stage
import pyarrow as pa
import pyarrow.parquet as pq

client = KL3MClient()

# Collect document tables and combine them
tables = []

for doc_id in client.iter_documents("usc", Stage.PARQUET, limit=20):
    document = client.get_document("usc", doc_id, Stage.PARQUET)
    parquet = document.get_parquet()
    
    if parquet:
        table = parquet.get_table()
        tables.append(table)

if tables:
    # Combine tables
    combined_table = pa.concat_tables(tables)
    
    # Write combined table to local parquet file
    pq.write_table(
        combined_table, 
        "combined_documents.parquet", 
        compression="snappy"
    )
    
    print(f"Combined {len(tables)} document tables:")
    print(f"  Total rows: {len(combined_table)}")
    print(f"  Columns: {combined_table.column_names}")
```

## Optimizing for Large Datasets

For very large datasets, optimize memory usage:

```python
from kl3m_data_client import KL3MClient
from kl3m_data_client.models.common import Stage
import gc

client = KL3MClient()

# Process a large dataset efficiently
with open("large_export.jsonl", "w") as output_file:
    for idx, doc in enumerate(client.iter_jsonl_export(
        dataset_id="usc",
        source_stage=Stage.PARQUET,
        max_documents=1000000  # Very large number
    )):
        # Write directly to file to avoid keeping in memory
        output_file.write(json.dumps(doc) + "\n")
        
        # Process in batches and release memory
        if idx > 0 and idx % 1000 == 0:
            print(f"Processed {idx} documents")
            gc.collect()  # Force garbage collection
```

## Direct S3 Integration

Advanced users can use the S3 utilities directly:

```python
from kl3m_data_client.utils.s3 import (
    get_s3_client,
    list_dataset_ids,
    get_stage_prefix,
    iter_prefix
)
import json

# Create S3 client
s3_client = get_s3_client()

# Get all datasets across stages
stages = ["documents", "representations", "parquet"]
dataset_availability = {}

for stage in stages:
    datasets = list_dataset_ids(s3_client, "data.kl3m.ai", stage)
    dataset_availability[stage] = datasets

# Find datasets available in all stages
common_datasets = set.intersection(
    *[set(dataset_availability[stage]) for stage in stages]
)

print(f"Datasets available in all stages: {common_datasets}")
```