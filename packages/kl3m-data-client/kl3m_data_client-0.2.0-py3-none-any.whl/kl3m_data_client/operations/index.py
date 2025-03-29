"""
Index operations for the KL3M data client.
"""

import json
import gzip
import datetime
import logging
from typing import Optional

import boto3

from kl3m_data_client.models.common import Stage
from kl3m_data_client.models.stage import DatasetIndex
from kl3m_data_client.utils.s3 import (
    get_object_bytes,
    put_object_bytes,
    get_index_key,
    iter_prefix,
)

logger = logging.getLogger("kl3m_data_client")


def build_dataset_index(
    s3_client: boto3.client,
    bucket: str,
    dataset_id: str,
    key_prefix: Optional[str] = None,
) -> bool:
    """
    Build an index for a dataset.

    Args:
        s3_client: S3 client.
        bucket: Bucket name.
        dataset_id: Dataset ID.
        key_prefix: Optional key prefix to filter objects.

    Returns:
        Whether the index was successfully built.
    """
    try:
        # Get all representation keys
        rep_prefix = f"{Stage.REPRESENTATIONS.value}/{dataset_id}/"
        if key_prefix:
            clean_prefix = key_prefix.strip("/")
            if clean_prefix:
                rep_prefix = f"{rep_prefix}{clean_prefix}/"

        # Collect all keys
        all_keys = list(iter_prefix(s3_client, bucket, rep_prefix))

        # Generate the index path
        index_path = get_index_key(dataset_id)

        # Add key_prefix to index path if specified
        if key_prefix:
            # Modify the index path to include key_prefix info
            if index_path.endswith(".json.gz"):
                clean_prefix = key_prefix.strip("/").replace("/", "-")
                index_path = index_path.replace(".json.gz", f"-{clean_prefix}.json.gz")

        # Create index content with metadata
        index_data = {
            "objects": all_keys,
            "metadata": {
                "dataset_id": dataset_id,
                "key_prefix": key_prefix,
                "count": len(all_keys),
                "created_at": datetime.datetime.now().isoformat(),
            },
        }

        # Compress the data
        compressed_data = gzip.compress(json.dumps(index_data).encode("utf-8"))

        # Upload the index
        result = put_object_bytes(s3_client, bucket, index_path, compressed_data)

        if result:
            logger.info(
                "Successfully built index with %d objects at %s",
                len(all_keys),
                index_path,
            )
        else:
            logger.error("Failed to upload index to %s", index_path)

        return result

    except Exception as e:
        logger.error("Error building index: %s", e)
        return False


def get_dataset_index(
    s3_client: boto3.client,
    bucket: str,
    dataset_id: str,
    key_prefix: Optional[str] = None,
) -> Optional[DatasetIndex]:
    """
    Get the index for a dataset.

    Args:
        s3_client: S3 client.
        bucket: Bucket name.
        dataset_id: Dataset ID.
        key_prefix: Optional key prefix used when building the index.

    Returns:
        The dataset index, or None if not found.
    """
    try:
        # Generate the index path
        index_path = get_index_key(dataset_id)

        # Add key_prefix to index path if specified
        if key_prefix:
            # Modify the index path to include key_prefix info
            if index_path.endswith(".json.gz"):
                clean_prefix = key_prefix.strip("/").replace("/", "-")
                index_path = index_path.replace(".json.gz", f"-{clean_prefix}.json.gz")

        # Get the compressed index data
        compressed_data = get_object_bytes(s3_client, bucket, index_path)
        if not compressed_data:
            logger.warning("Index not found: %s", index_path)
            return None

        # Decompress and parse the index
        try:
            decompressed_data = gzip.decompress(compressed_data)
            index_data = json.loads(decompressed_data)
            return DatasetIndex.from_dict(index_data)
        except Exception as e:
            logger.error("Error parsing index: %s", e)
            return None

    except Exception as e:
        logger.error("Error getting index: %s", e)
        return None
