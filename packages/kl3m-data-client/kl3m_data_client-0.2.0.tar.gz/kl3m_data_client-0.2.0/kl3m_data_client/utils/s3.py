"""
S3 utility functions for the KL3M data client.

This module contains functionality from the original kl3m_data/utils/s3_utils.py,
adapted for the client package.
"""

import time
import zlib
import base64
import logging
from pathlib import Path
from typing import Generator, Optional, List, Union

import boto3
import botocore.config

from kl3m_data_client.models.common import Stage
from kl3m_data_client.utils.boto_types import S3ClientType


# Default timeout for S3 operations
DEFAULT_TIMEOUT = 600

# Set up logging
logger = logging.getLogger("kl3m_data_client")


def get_s3_config(
    pool_size: int = 25,  # Larger connection pool for better parallelism
    connect_timeout: int = 10,  # Shorter connect timeout
    read_timeout: int = 60,  # Longer read timeout
    retry_count: int = 3,  # More retries
    retry_mode: str = "adaptive",  # Adaptive retries
    region_name: Optional[str] = None,
) -> botocore.config.Config:
    """
    Get an optimized S3 configuration object with the specified parameters.

    Args:
        pool_size: Number of connections in the pool.
        connect_timeout: Connection timeout in seconds.
        read_timeout: Read timeout in seconds.
        retry_count: Number of retries.
        retry_mode: Retry mode ('standard', 'adaptive', or 'legacy').
        region_name: AWS region name.

    Returns:
        An optimized S3 configuration object.
    """
    # Create a new configuration with optimized defaults
    config_dict = {
        "max_pool_connections": pool_size,
        "connect_timeout": connect_timeout,
        "read_timeout": read_timeout,
        "retries": {
            "max_attempts": retry_count,
            "mode": retry_mode,
        },
    }

    if region_name is not None:
        config_dict["region_name"] = region_name

    # Create config from dictionary
    config = botocore.config.Config(**config_dict)

    # Log configuration details
    logger.info(
        "S3 configured with region=%s, pool_size=%s, connect_timeout=%s, read_timeout=%s, retry_count=%s, retry_mode=%s",
        region_name,
        pool_size,
        connect_timeout,
        read_timeout,
        retry_count,
        retry_mode,
    )

    return config


def get_s3_client(
    aws_access_key_id: Optional[str] = None,
    aws_secret_access_key: Optional[str] = None,
    aws_session_token: Optional[str] = None,
    region_name: Optional[str] = None,
    config: Optional[botocore.config.Config] = None,
) -> S3ClientType:
    """
    Get an S3 client with the specified configuration.

    Args:
        aws_access_key_id: AWS access key ID.
        aws_secret_access_key: AWS secret access key.
        aws_session_token: AWS session token.
        region_name: AWS region name.
        config: S3 configuration object.

    Returns:
        An S3 client.
    """
    # get default if not provided
    if config is None:
        config = get_s3_config(region_name=region_name)

    # create the S3 client
    client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        aws_session_token=aws_session_token,
        config=config,
    )

    return client


def put_object_bytes(
    client: S3ClientType,
    bucket: str,
    key: str,
    data: Union[str, bytes],
    retry_count: int = 3,
    retry_delay: float = 1.0,
) -> bool:
    """
    Put an object into an S3 bucket with improved retry logic.

    Args:
        client: S3 client.
        bucket: Bucket name.
        key: Object key.
        data: Object data.
        retry_count: Number of retries on failure.
        retry_delay: Base delay between retries in seconds.

    Returns:
        Whether the operation succeeded.
    """
    # encode the data if it is a string
    if isinstance(data, str):
        data = data.encode("utf-8")

    # put the object into the bucket with exponential backoff retry
    for attempt in range(retry_count + 1):
        try:
            # put the object
            client.put_object(
                Bucket=bucket,
                Key=key,
                Body=data,
            )

            if attempt > 0:
                logger.info(
                    "Put object %s/%s (%d bytes) after %d retries",
                    bucket,
                    key,
                    len(data),
                    attempt,
                )
            else:
                logger.info("Put object %s/%s (%d bytes)", bucket, key, len(data))

            return True

        except Exception as e:
            if attempt < retry_count:
                # Calculate exponential backoff delay
                backoff_delay = retry_delay * (2**attempt)
                logger.warning(
                    "Error putting object %s/%s: %s. Retrying in %.1f seconds... (%d/%d)",
                    bucket,
                    key,
                    e,
                    backoff_delay,
                    attempt + 1,
                    retry_count,
                )
                time.sleep(backoff_delay)
            else:
                logger.error(
                    "Error putting object %s/%s after %d retries: %s",
                    bucket,
                    key,
                    retry_count,
                    e,
                )
                return False

    return False


def put_object_path(
    client: S3ClientType, bucket: str, key: str, path: Union[str, Path]
) -> bool:
    """
    Put an object into an S3 bucket.

    Args:
        client: S3 client.
        bucket: Bucket name.
        key: Object key.
        path: Path to the object.

    Returns:
        Whether the operation succeeded.
    """
    # read the object data
    try:
        with open(path, "rb") as input_file:
            data = input_file.read()
    except Exception as e:
        logger.error("Error reading object data: %s", e)
        return False

    # put the object into the bucket
    return put_object_bytes(client, bucket, key, data)


def get_object_bytes(
    client: S3ClientType,
    bucket: str,
    key: str,
    retry_count: int = 3,
    retry_delay: float = 1.0,
) -> Optional[bytes]:
    """
    Get an object from an S3 bucket with improved retry logic.

    Args:
        client: S3 client.
        bucket: Bucket name.
        key: Object key.
        retry_count: Number of retries on failure.
        retry_delay: Delay between retries in seconds.

    Returns:
        Object data as bytes, or None if an error occurs.
    """
    # Implement exponential backoff retry
    for attempt in range(retry_count + 1):
        try:
            response = client.get_object(
                Bucket=bucket,
                Key=key,
            )

            # Stream and read content in chunks if needed
            data = response["Body"].read()

            if attempt > 0:
                logger.info(
                    "Got object %s://%s after %d retries (%d bytes)",
                    bucket,
                    key,
                    attempt,
                    len(data),
                )
            else:
                logger.info("Got object %s://%s (%d bytes)", bucket, key, len(data))

            return data

        except client.exceptions.NoSuchKey:
            # Don't retry if the key doesn't exist
            logger.error("Object %s://%s does not exist", bucket, key)
            return None

        except Exception as e:
            if attempt < retry_count:
                # Calculate exponential backoff delay
                backoff_delay = retry_delay * (2**attempt)
                logger.warning(
                    "Error getting object %s://%s: %s. Retrying in %.1f seconds... (%d/%d)",
                    bucket,
                    key,
                    e,
                    backoff_delay,
                    attempt + 1,
                    retry_count,
                )
                time.sleep(backoff_delay)
            else:
                logger.error(
                    "Error getting object %s://%s after %d retries: %s",
                    bucket,
                    key,
                    retry_count,
                    e,
                )
                return None

    return None


def get_object(
    client: S3ClientType,
    bucket: str,
    key: str,
    retry_count: int = 3,
    retry_delay: float = 1.0,
) -> Optional[str]:
    """
    Get an object from an S3 bucket and return it as a string with improved retry logic.

    Args:
        client: S3 client.
        bucket: Bucket name.
        key: Object key.
        retry_count: Number of retries on failure.
        retry_delay: Delay between retries in seconds.

    Returns:
        Object data as a UTF-8 string, or None if an error occurs.
    """
    # Get the object as bytes
    data_bytes = get_object_bytes(client, bucket, key, retry_count, retry_delay)

    # Convert to string if we got data
    if data_bytes is not None:
        try:
            return data_bytes.decode("utf-8")
        except UnicodeDecodeError as e:
            logger.error("Error decoding object %s://%s: %s", bucket, key, e)
            return None

    return None


def check_object_exists(
    client: S3ClientType,
    bucket: str,
    key: str,
    retry_count: int = 2,
    retry_delay: float = 0.5,
) -> bool:
    """
    Check if an object exists in an S3 bucket with improved retry logic.

    Args:
        client: S3 client.
        bucket: Bucket name.
        key: Object key.
        retry_count: Number of retries on failure.
        retry_delay: Delay between retries in seconds.

    Returns:
        Whether the object exists.
    """
    # check if the object exists with retries
    for attempt in range(retry_count + 1):
        try:
            client.head_object(
                Bucket=bucket,
                Key=key,
            )
            return True

        except client.exceptions.ClientError as e:
            # If the error is 404, the object doesn't exist
            if e.response["Error"]["Code"] == "404":
                return False

            # For other client errors, retry if we have attempts left
            if attempt < retry_count:
                backoff_delay = retry_delay * (2**attempt)
                logger.warning(
                    "Error checking if object %s/%s exists: %s. Retrying in %.1f seconds... (%d/%d)",
                    bucket,
                    key,
                    e,
                    backoff_delay,
                    attempt + 1,
                    retry_count,
                )
                time.sleep(backoff_delay)
            else:
                logger.error(
                    "Error checking if object %s/%s exists after %d retries: %s",
                    bucket,
                    key,
                    retry_count,
                    e,
                )
                return False

        except Exception as e:
            if attempt < retry_count:
                backoff_delay = retry_delay * (2**attempt)
                logger.warning(
                    "Error checking if object %s/%s exists: %s. Retrying in %.1f seconds... (%d/%d)",
                    bucket,
                    key,
                    e,
                    backoff_delay,
                    attempt + 1,
                    retry_count,
                )
                time.sleep(backoff_delay)
            else:
                logger.error(
                    "Error checking if object %s/%s exists after %d retries: %s",
                    bucket,
                    key,
                    retry_count,
                    e,
                )
                return False

    return False


def check_prefix_exists(
    client: S3ClientType,
    bucket: str,
    prefix: str,
) -> bool:
    """
    Check if a prefix exists in an S3 bucket.

    Args:
        client: S3 client.
        bucket: Bucket name.
        prefix: Prefix.

    Returns:
        Whether the prefix exists.
    """
    # check if the prefix exists
    try:
        response = client.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix,
        )
        return "Contents" in response
    except Exception as e:
        logger.error("Error checking prefix: %s", e)
        return False


def list_common_prefixes(
    client: S3ClientType,
    bucket: str,
    prefix: str,
) -> List[str]:
    """
    List the common prefixes, i.e., "folders", with a prefix in an S3 bucket.

    Args:
        client: S3 client.
        bucket: Bucket name.
        prefix: Prefix.

    Returns:
        List of common prefixes.
    """
    # get the objects with the prefix
    try:
        response = client.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix,
            Delimiter="/",
        )
        if "CommonPrefixes" in response:
            return [obj["Prefix"] for obj in response["CommonPrefixes"]]
    except Exception as e:
        logger.error("Error listing prefix: %s", e)
    return []


def iter_prefix(
    client: S3ClientType,
    bucket: str,
    prefix: str,
    page_size: int = 1000,
    max_items: Optional[int] = None,
) -> Generator[str, None, None]:
    """
    Iterate over objects with a prefix in an S3 bucket with optimized pagination.

    Args:
        client: S3 client.
        bucket: Bucket name.
        prefix: Prefix.
        page_size: Number of keys to retrieve per request.
        max_items: Maximum number of items to retrieve.

    Yields:
        Object key.
    """
    # get the objects with the prefix
    try:
        list_paginator = client.get_paginator("list_objects_v2")
        pagination_config = {
            "PageSize": page_size,  # Retrieve more keys per request
        }

        if max_items:
            pagination_config["MaxItems"] = max_items

        list_results = list_paginator.paginate(
            Bucket=bucket, Prefix=prefix, PaginationConfig=pagination_config
        )

        for results in list_results:
            if "Contents" in results:
                # Process all keys in one batch for better performance
                for obj in results["Contents"]:
                    yield obj["Key"]
    except Exception as e:
        logger.error("Error listing prefix: %s", e)


def get_stage_prefix(stage: Stage, dataset_id: Optional[str] = None) -> str:
    """
    Get the S3 prefix for a specific stage and optional dataset ID.

    Args:
        stage: The storage stage
        dataset_id: The dataset ID (optional)

    Returns:
        The S3 prefix
    """
    if stage == Stage.INDEX:
        return f"{stage.value}/"
    elif dataset_id:
        return f"{stage.value}/{dataset_id}/"
    else:
        return f"{stage.value}/"


def convert_key_to_stage(key: str, target_stage: Stage) -> str:
    """
    Convert an S3 key from its current stage to the target stage.

    Args:
        key: The S3 key to convert
        target_stage: The target storage stage

    Returns:
        The converted S3 key
    """
    logger.debug("Converting key '%s' to stage '%s'", key, target_stage.value)

    # Split the key into components
    components = key.split("/")

    if len(components) < 2:
        raise ValueError(f"Invalid key format: {key}")

    # Save the original stage
    original_stage = components[0]

    # Replace the first component with the target stage
    components[0] = target_stage.value

    # For parquet, we need to handle extension differently
    if target_stage == Stage.PARQUET:
        # Always remove the .json extension when converting to parquet
        if key.endswith(".json"):
            result = "/".join(components)[: -len(".json")]
            logger.debug(
                "Converted '%s' from '%s' to '%s': '%s' (removed .json)",
                key,
                original_stage,
                target_stage.value,
                result,
            )
            return result
        else:
            # Key doesn't end with .json - e.g., when converting from parquet to parquet
            result = "/".join(components)
            logger.debug(
                "Converted '%s' from '%s' to '%s': '%s' (no extension change)",
                key,
                original_stage,
                target_stage.value,
                result,
            )
            return result

    # For document and representation stages, we need to ensure proper extension
    elif target_stage in [Stage.DOCUMENTS, Stage.REPRESENTATIONS]:
        # If converting from parquet (no extension) to documents/representations, add .json
        if original_stage == Stage.PARQUET.value and not key.endswith(".json"):
            result = "/".join(components) + ".json"
            logger.debug(
                "Converted '%s' from '%s' to '%s': '%s' (added .json)",
                key,
                original_stage,
                target_stage.value,
                result,
            )
            return result

    # Default case - just change the stage prefix
    result = "/".join(components)
    logger.debug(
        "Converted '%s' from '%s' to '%s': '%s' (stage prefix only)",
        key,
        original_stage,
        target_stage.value,
        result,
    )
    return result


def get_document_key(key: str) -> str:
    """
    Convert any key to a document key.

    Args:
        key: The S3 key to convert

    Returns:
        The document key
    """
    return convert_key_to_stage(key, Stage.DOCUMENTS)


def get_representation_key(key: str) -> str:
    """
    Convert any key to a representation key.

    Args:
        key: The S3 key to convert

    Returns:
        The representation key
    """
    return convert_key_to_stage(key, Stage.REPRESENTATIONS)


def get_parquet_key(key: str) -> str:
    """
    Convert any key to a parquet key (removes .json extension if present).

    Args:
        key: The S3 key to convert

    Returns:
        The parquet key
    """
    return convert_key_to_stage(key, Stage.PARQUET)


def get_index_key(dataset_id: str) -> str:
    """
    Get the index key for a dataset.

    Args:
        dataset_id: The dataset ID

    Returns:
        The index key
    """
    return f"{Stage.INDEX.value}/{dataset_id}.json.gz"


def check_stage_exists(
    client: S3ClientType,
    bucket: str,
    key: str,
    stage: Stage,
    retry_count: int = 2,
    retry_delay: float = 0.5,
) -> bool:
    """
    Check if an object exists in a specific S3 stage.

    Args:
        client: S3 client
        bucket: Bucket name
        key: The original key (from any stage)
        stage: The stage to check
        retry_count: Number of retries on failure
        retry_delay: Delay between retries in seconds

    Returns:
        Whether the object exists in the specified stage
    """
    # Convert the key to the target stage
    stage_key = convert_key_to_stage(key, stage)

    # Log the check
    logger.debug("Checking if object exists in %s stage: %s", stage.value, stage_key)

    # Check if the object exists
    result = check_object_exists(client, bucket, stage_key, retry_count, retry_delay)

    # Log the result
    if result:
        logger.debug("Object exists in %s stage: %s", stage.value, stage_key)
    else:
        logger.debug("Object does NOT exist in %s stage: %s", stage.value, stage_key)

    return result


def list_dataset_ids(
    client: S3ClientType,
    bucket: str,
    stage: Stage = Stage.DOCUMENTS,
) -> List[str]:
    """
    List all dataset IDs available in a specific stage.

    Args:
        client: S3 client
        bucket: Bucket name
        stage: The stage to list datasets from

    Returns:
        List of dataset IDs
    """
    # Get the prefix for the stage
    prefix = get_stage_prefix(stage)

    # List common prefixes
    common_prefixes = list_common_prefixes(client, bucket, prefix)

    # Extract dataset IDs from prefixes
    dataset_ids = []
    for prefix in common_prefixes:
        # Extract dataset ID from prefix (format: "stage/dataset_id/")
        parts = prefix.rstrip("/").split("/")
        if len(parts) >= 2:
            dataset_ids.append(parts[1])

    return dataset_ids


def decompress_content(content: str, binary: bool = False) -> Union[str, bytes]:
    """
    Decompress base64-encoded zlib-compressed content.

    Args:
        content: The base64-encoded zlib-compressed content.
        binary: If True, return raw bytes instead of attempting UTF-8 decoding.
               This is useful for binary content like PDFs.

    Returns:
        The decompressed content as a string or bytes depending on the binary flag.
    """
    try:
        # Decode base64
        decoded = base64.b64decode(content)
        # Decompress zlib
        decompressed = zlib.decompress(decoded)

        # Return raw bytes for binary content
        if binary:
            return decompressed

        # Try to decode as UTF-8 for text content
        try:
            return decompressed.decode("utf-8")
        except UnicodeDecodeError:
            # The content is binary (PDF, image, etc.) but we weren't explicitly told
            # No need to log a warning since this is expected for binary content
            # Return bytes if UTF-8 decoding fails
            return decompressed
    except Exception as e:
        logger.error("Error decompressing content: %s", e)
        return b"" if binary else ""
