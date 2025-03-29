# Command Line Interface Reference

The KL3M Data Client provides a comprehensive command-line interface through the `kl3m-client` command.

## Global Options

These options apply to all commands:

```
--verbose            Enable verbose output
--help, -h           Show help message and exit
```

## Available Commands

### List Datasets

List all available datasets:

```bash
kl3m-client list
```

Options:
- `--json`: Output in JSON format

### Dataset Status

Show detailed status information for a dataset:

```bash
kl3m-client status <dataset_id>
```

Options:
- `--json`: Output in JSON format

### List Documents

List documents in a dataset:

```bash
kl3m-client documents <dataset_id>
```

Options:
- `--stage`: Pipeline stage to use (documents, representations, parquet)
- `--limit`: Limit the number of documents shown
- `--count`: Only show document count
- `--json`: Output in JSON format

### Inspect Document

Inspect a specific document:

```bash
kl3m-client inspect <dataset_id> <document_id>
```

Options:
- `--stage`: Pipeline stage to use (documents, representations, parquet)
- `--json`: Output in JSON format

### Export to JSONL

Export a dataset to JSONL format:

```bash
kl3m-client export-jsonl <dataset_id> --output <output_file.jsonl>
```

Options:
- `--output`: Path to output file (required)
- `--stage`: Source stage for export (default: parquet)
- `--max-documents`: Limit number of documents to export
- `--no-deduplicate`: Disable document deduplication
- `--compress`: Compress output with gzip
- `--exclude-content`: Exclude document content from export
- `--verbose`: Show progress and details during export

## Examples

```bash
# List all datasets
kl3m-client list

# Show detailed status for the USC dataset
kl3m-client status usc

# List first 10 documents in the CAP dataset
kl3m-client documents cap --limit 10 --stage documents

# Inspect a specific document
kl3m-client inspect cap 12345 --stage parquet

# Export 1000 documents from USC dataset to JSONL
kl3m-client export-jsonl usc --output usc-export.jsonl --max-documents 1000 --compress
```

## Environment Variables

The CLI respects the following environment variables:

- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `AWS_DEFAULT_REGION`: AWS region
- `AWS_PROFILE`: AWS profile to use