# AWS Integration

The KL3M Data Client uses AWS S3 to access and manage dataset files. This guide explains the AWS integration features and authentication options.

## Authentication Methods

The client supports all standard AWS authentication methods:

1. **Environment Variables**:
   ```bash
   export AWS_ACCESS_KEY_ID=your_access_key
   export AWS_SECRET_ACCESS_KEY=your_secret_key
   export AWS_DEFAULT_REGION=us-east-1
   ```

2. **Shared Credentials File**:
   The client will use credentials stored in `~/.aws/credentials` if available.

3. **AWS Config File**:
   Configuration in `~/.aws/config` will be used if available.

4. **IAM Role for EC2**:
   If running on EC2, the client can use the attached IAM role permissions.

5. **Explicit Credentials**:
   ```python
   client = KL3MClient(
       aws_access_key_id="your_access_key",
       aws_secret_access_key="your_secret_key",
       region="us-east-1"
   )
   ```

## S3 Bucket Configuration

By default, the client connects to the `data.kl3m.ai` bucket. You can specify a different bucket:

```python
client = KL3MClient(bucket_name="your-bucket-name")
```

## Low-level S3 Utilities

The library exposes low-level S3 utilities for advanced usage:

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

# Get an S3 client directly
s3_client = get_s3_client(
    region="us-east-1",
    aws_access_key_id="your_access_key",
    aws_secret_access_key="your_secret_key"
)

# List datasets directly
datasets = list_dataset_ids(s3_client, "data.kl3m.ai", Stage.DOCUMENTS)

# Stream keys with a prefix
for key in iter_prefix(s3_client, "data.kl3m.ai", "documents/usc/"):
    # Process each key
    pass

# Check if object exists
exists = check_object_exists(s3_client, "data.kl3m.ai", "documents/usc/123")

# Get object content
content_bytes = get_object_bytes(s3_client, "data.kl3m.ai", "documents/usc/123")

# Decompress content if needed
if key.endswith(".gz"):
    decompressed = decompress_content(content_bytes)
```

## Performance Considerations

- The client supports concurrent operations for retrieving multiple documents
- For large datasets, use streaming iterators (`iter_documents`, `iter_jsonl_export`)
- Consider filtering data on the S3 side when possible
- Use the `verbose` flag to see operation progress for long-running tasks

## Security Best Practices

1. Use IAM roles with minimal permissions needed
2. Never hardcode credentials in your application code
3. Consider using temporary credentials for short-lived operations
4. Store AWS credentials securely and rotate regularly
5. Use VPC endpoints for enhanced security if available