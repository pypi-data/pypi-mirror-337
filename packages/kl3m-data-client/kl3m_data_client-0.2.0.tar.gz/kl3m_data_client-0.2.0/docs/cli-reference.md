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


## Examples

### Basic Usage

```bash
# List all datasets
kl3m-client list

# Show detailed status for the USC dataset
kl3m-client status usc

# List first 10 documents in the CAP dataset
kl3m-client documents cap --limit 10 --stage documents

# Inspect a specific document
kl3m-client inspect cap 12345 --stage parquet
```

### JSON Output Examples

The CLI supports JSON output for all commands using the `--json` flag. Here are examples with their outputs:

#### List datasets with JSON output

```bash
kl3m-client list --json
```

Output:
```json
{
  "govinfo": {
    "documents": true,
    "representations": true,
    "parquet": true
  },
  "ukleg": {
    "documents": true,
    "representations": true,
    "parquet": true
  },
  "usc": {
    "documents": true,
    "representations": true,
    "parquet": true
  },
  "cap": {
    "documents": true,
    "representations": true,
    "parquet": true
  }
  // Additional datasets omitted for brevity
}
```

#### Show dataset status with JSON output

```bash
kl3m-client status usc --json
```

Output:
```json
{
  "dataset_id": "usc",
  "document_count": 69391,
  "representation_count": 69391,
  "parquet_count": 69391,
  "missing_representations": 0,
  "missing_parquet": 0,
  "is_complete": true
}
```

#### List documents with JSON output

```bash
kl3m-client documents usc --stage documents --limit 5 --json
```

Output:
```json
{
  "dataset_id": "usc",
  "stage": "documents",
  "document_count": 5,
  "documents": [
    "118/66/10_-Subtitle_A-ptI-ch1",
    "118/66/10_-Subtitle_A-ptI-ch11",
    "118/66/10_-Subtitle_A-ptI-ch12",
    "118/66/10_-Subtitle_A-ptI-ch13",
    "118/66/10_-Subtitle_A-ptI-ch14"
  ]
}
```

#### Get document count with JSON output

```bash
kl3m-client documents usc --stage documents --count --limit 10 --json
```

Output:
```json
{
  "dataset_id": "usc",
  "stage": "documents",
  "document_count": 10
}
```

#### Inspect document with JSON output

```bash
kl3m-client inspect usc "118/66/10_-Subtitle_A-ptI-ch1" --stage documents --json
```

Output:
```json
{
  "dataset_id": "usc",
  "document_id": "118/66/10_-Subtitle_A-ptI-ch1",
  "stage": "documents",
  "content_type": "document",
  "metadata": {
    "identifier": "https://uscode.house.gov/download/releasepoints/us/pl/118/66/htm_usc10@118-66.zip#10_-Subtitle_A-ptI-ch1",
    "source": "",
    "title": "",
    "format": "application/xhtml+xml"
  },
  "content_preview": "<div><h3 class=\"chapter-head\"><strong>CHAPTER 1—DEFINITIONS, RULES OF CONSTRUCTION, CROSS REFERENCES, AND RELATED MATTERS</strong></h3>\r\n<!-- field-end:structuralhead -->\r\n<!-- field-start:analysis --"
}
```

## Environment Variables

The CLI respects the following environment variables:

- `AWS_ACCESS_KEY_ID`: AWS access key
- `AWS_SECRET_ACCESS_KEY`: AWS secret key
- `AWS_DEFAULT_REGION`: AWS region
- `AWS_PROFILE`: AWS profile to use