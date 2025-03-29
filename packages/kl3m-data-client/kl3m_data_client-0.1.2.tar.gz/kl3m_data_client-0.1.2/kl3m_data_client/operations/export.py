"""
Export operations for the KL3M data client.
"""

import os
import json
import logging
import hashlib
from typing import Optional, Generator

import boto3

from kl3m_data_client.models.common import Stage
from kl3m_data_client.utils.s3 import (
    get_object_bytes,
    iter_prefix,
    decompress_content,
)

logger = logging.getLogger("kl3m_data_client")


def iter_jsonl_export(
    s3_client: boto3.client,
    bucket: str,
    dataset_id: str,
    source_stage: Stage = Stage.PARQUET,
    key_prefix: Optional[str] = None,
    max_documents: Optional[int] = None,
    tokenizer: str = "cl100k_base",
    representation: str = "text/plain",
    deduplicate: bool = True,
    include_metrics: bool = False,
) -> Generator[dict, None, None]:
    """
    Iterate over documents in a dataset for export to JSONL, yielding each document as it is processed.

    This streaming approach is memory-efficient for large datasets.

    Args:
        s3_client: S3 client.
        bucket: Bucket name.
        dataset_id: Dataset ID to export.
        source_stage: Source stage to export from (REPRESENTATIONS or PARQUET).
        key_prefix: Optional key prefix to filter objects.
        max_documents: Maximum number of documents to export.
        tokenizer: Tokenizer name to use for token extraction.
        representation: Representation MIME type.
        deduplicate: Whether to deduplicate documents.
        include_metrics: Whether to include detailed metrics in the output.

    Yields:
        Processed documents ready for JSONL export.
    """
    if source_stage not in [Stage.REPRESENTATIONS, Stage.PARQUET]:
        raise ValueError(
            f"Invalid source stage for export: {source_stage}. Must be REPRESENTATIONS or PARQUET."
        )

    # Format prefix
    prefix = f"{source_stage.value}/{dataset_id}/"
    if key_prefix:
        clean_prefix = key_prefix.strip("/")
        if clean_prefix:
            prefix = f"{prefix}{clean_prefix}/"

    logger.info("Streaming %s from %s for export", dataset_id, source_stage.value)

    # Set up counters
    count = 0
    deduplication_hashes = set()

    # Iterate through all objects
    for key in iter_prefix(s3_client, bucket, prefix, max_items=max_documents):
        try:
            # Initialize variables that will be used throughout
            tokens = []
            text_content = ""
            metadata = {}
            document = {}
            # Get object data
            object_data = get_object_bytes(s3_client, bucket, key)
            if not object_data:
                logger.warning("Failed to retrieve object %s", key)
                continue

            # Parse the object data
            if source_stage == Stage.REPRESENTATIONS:
                # Extract from representations format
                doc_data = json.loads(object_data)
                if "documents" not in doc_data or not doc_data["documents"]:
                    logger.warning("No documents found in %s", key)
                    continue

                # Get the first document
                document = doc_data["documents"][0]

                # Extract tokens from the specified representation
                if (
                    "representations" not in document
                    or representation not in document["representations"]
                ):
                    logger.warning(
                        "Representation %s not found in %s",
                        representation, key
                    )
                    continue

                rep = document["representations"][representation]

                # Extract compressed content if needed
                if "content" in rep and isinstance(rep["content"], str):
                    text_content = decompress_content(rep["content"])
                else:
                    text_content = rep.get("content", "")

                # Extract tokens
                if "tokens" in rep and tokenizer in rep["tokens"]:
                    tokens = rep["tokens"][tokenizer]
                else:
                    tokens = []

                # Extract metadata
                metadata = document.get("metadata", {})

            elif source_stage == Stage.PARQUET:
                # In a real implementation, this would parse parquet
                # Here we'll assume the parquet is actually JSON (simplification)
                document = json.loads(object_data)

                # Extract from the representation
                if (
                    "representations" not in document
                    or representation not in document["representations"]
                ):
                    logger.warning(
                        "Representation %s not found in %s",
                        representation, key
                    )
                    continue

                rep = document["representations"][representation]

                # Extract compressed content if needed
                if "content" in rep and isinstance(rep["content"], str):
                    text_content = decompress_content(rep["content"])
                else:
                    text_content = rep.get("content", "")

                # Extract tokens
                if "tokens" in rep and tokenizer in rep["tokens"]:
                    tokens = rep["tokens"][tokenizer]
                else:
                    tokens = []

                # Extract metadata
                metadata = document.get("metadata", {})

            # Skip if no tokens
            if not tokens:
                logger.warning("No tokens found in %s", key)
                continue

            # Check for duplicates if deduplication is enabled
            if deduplicate:
                # Create a hash of the tokens
                token_hash = hashlib.md5(str(tokens).encode()).hexdigest()

                # Skip if we've seen this hash before
                if token_hash in deduplication_hashes:
                    logger.debug("Skipping duplicate document: %s", key)
                    continue

                # Add to our set of seen hashes
                deduplication_hashes.add(token_hash)

            # Prepare the output document
            output_doc = {
                "id": document.get("identifier", os.path.basename(key)),
                "text": text_content,
                "tokens": tokens,
                "metadata": {
                    "source": document.get("source", ""),
                    "dataset": dataset_id,
                    "title": metadata.get("title", ""),
                    "date": metadata.get("date", ""),
                },
            }

            # Add metrics if requested
            if include_metrics and "metrics" in document:
                output_doc["metrics"] = document["metrics"]

            # Yield the document for processing
            yield output_doc
            count += 1

            # Log progress
            if count % 1000 == 0:
                logger.info("Processed %d documents...", count)

        except Exception as e:
            logger.error("Error processing %s: %s", key, e)

    logger.info("Stream complete. Processed %d documents.", count)


def export_to_jsonl(
    s3_client: boto3.client,
    bucket: str,
    dataset_id: str,
    output_path: str,
    source_stage: Stage = Stage.PARQUET,
    key_prefix: Optional[str] = None,
    max_documents: Optional[int] = None,
    tokenizer: str = "cl100k_base",
    representation: str = "text/plain",
    deduplicate: bool = True,
    include_metrics: bool = False,
) -> int:
    """
    Export dataset documents to a JSONL file.

    Args:
        s3_client: S3 client.
        bucket: Bucket name.
        dataset_id: Dataset ID to export.
        output_path: Path to output JSONL file.
        source_stage: Source stage to export from (REPRESENTATIONS or PARQUET).
        key_prefix: Optional key prefix to filter objects.
        max_documents: Maximum number of documents to export.
        tokenizer: Tokenizer name to use for token extraction.
        representation: Representation MIME type.
        deduplicate: Whether to deduplicate documents.
        include_metrics: Whether to include detailed metrics in the output.

    Returns:
        Number of documents exported.
    """
    if source_stage not in [Stage.REPRESENTATIONS, Stage.PARQUET]:
        raise ValueError(
            f"Invalid source stage for export: {source_stage}. Must be REPRESENTATIONS or PARQUET."
        )

    # Ensure output directory exists
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

    logger.info("Exporting %s from %s to %s", dataset_id, source_stage.value, output_path)

    # Use streaming iterator to process documents
    count = 0
    with open(output_path, "w", encoding="utf-8") as out_file:
        # Iterate through documents using the streaming generator
        for document in iter_jsonl_export(
            s3_client,
            bucket,
            dataset_id,
            source_stage,
            key_prefix,
            max_documents,
            tokenizer,
            representation,
            deduplicate,
            include_metrics,
        ):
            # Write document to output file
            out_file.write(json.dumps(document) + "\n")
            count += 1

    logger.info("Export complete. Exported %d documents to %s", count, output_path)
    return count
