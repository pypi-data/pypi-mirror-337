"""
Main client class for interacting with KL3M data in S3.
"""

import logging
from typing import Dict, List, Optional, Generator

import boto3

from kl3m_data_client.models.common import Stage, DatasetStatus
from kl3m_data_client.document import Document
from kl3m_data_client.utils.s3 import (
    get_s3_client,
    list_dataset_ids,
    get_stage_prefix,
    iter_prefix,
)
from kl3m_data_client.utils.console import configure_logging
from kl3m_data_client.operations.export import (
    export_to_jsonl,
)
from kl3m_data_client.operations.index import (
    get_dataset_index,
)


logger = logging.getLogger("kl3m_data_client")


class KL3MClient:
    """Client for interacting with KL3M data in S3."""

    def __init__(
        self,
        bucket: str = "data.kl3m.ai",
        region: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        s3_client: Optional[boto3.client] = None,
        verbose: bool = False,
    ):
        """
        Initialize the KL3M data client.

        Args:
            bucket: S3 bucket name.
            region: AWS region.
            aws_access_key_id: AWS access key ID.
            aws_secret_access_key: AWS secret access key.
            aws_session_token: AWS session token.
            s3_client: Optional boto3 S3 client to use instead of creating a new one.
            verbose: Whether to enable verbose logging.
        """
        # Configure logging
        configure_logging(verbose)

        # Set up the S3 client
        self.bucket = bucket
        self.s3_client = s3_client or get_s3_client(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=region,
        )

        logger.info("Initialized KL3MClient for bucket %s", bucket)

    def list_datasets(self) -> Dict[str, Dict[Stage, bool]]:
        """
        List all available datasets.

        Returns:
            Dictionary mapping dataset IDs to a dictionary of stages to boolean values
            indicating whether the dataset has data in that stage.
        """
        logger.info("Listing available datasets")

        # Get datasets from each stage
        document_datasets = set(
            list_dataset_ids(self.s3_client, self.bucket, Stage.DOCUMENTS)
        )
        representation_datasets = set(
            list_dataset_ids(self.s3_client, self.bucket, Stage.REPRESENTATIONS)
        )
        parquet_datasets = set(
            list_dataset_ids(self.s3_client, self.bucket, Stage.PARQUET)
        )

        # Get all unique dataset IDs
        all_datasets = document_datasets.union(representation_datasets).union(
            parquet_datasets
        )

        # Create result dictionary
        result = {}
        for dataset_id in all_datasets:
            result[dataset_id] = {
                Stage.DOCUMENTS: dataset_id in document_datasets,
                Stage.REPRESENTATIONS: dataset_id in representation_datasets,
                Stage.PARQUET: dataset_id in parquet_datasets,
            }

        logger.info("Found %d datasets", len(result))
        return result

    def get_dataset_status(
        self, dataset_id: str, key_prefix: Optional[str] = None
    ) -> DatasetStatus:
        """
        Get the status of a dataset across all pipeline stages.

        Args:
            dataset_id: Dataset ID.
            key_prefix: Optional key prefix to filter objects.

        Returns:
            Dataset status.
        """
        logger.info("Getting status for dataset %s", dataset_id)

        # Initialize document counts
        doc_count = 0
        rep_count = 0
        parquet_count = 0

        # Adjusted prefixes for each stage
        doc_prefix = get_stage_prefix(Stage.DOCUMENTS, dataset_id)
        rep_prefix = get_stage_prefix(Stage.REPRESENTATIONS, dataset_id)
        parquet_prefix = get_stage_prefix(Stage.PARQUET, dataset_id)

        # Add key_prefix if specified
        if key_prefix:
            clean_prefix = key_prefix.strip("/")
            if clean_prefix:
                doc_prefix = f"{doc_prefix}{clean_prefix}/"
                rep_prefix = f"{rep_prefix}{clean_prefix}/"
                parquet_prefix = f"{parquet_prefix}{clean_prefix}/"

        # Count documents in each stage
        for _ in iter_prefix(self.s3_client, self.bucket, doc_prefix):
            doc_count += 1

        for _ in iter_prefix(self.s3_client, self.bucket, rep_prefix):
            rep_count += 1

        for _ in iter_prefix(self.s3_client, self.bucket, parquet_prefix):
            parquet_count += 1

        # Calculate missing documents by getting counts
        # We don't need to calculate the actual missing document keys
        missing_rep = max(0, doc_count - rep_count)
        missing_parquet = max(0, rep_count - parquet_count)

        # Create and return status
        return DatasetStatus(
            dataset_id=dataset_id,
            document_count=doc_count,
            representation_count=rep_count,
            parquet_count=parquet_count,
            missing_representations=missing_rep,
            missing_parquet=missing_parquet,
        )

    def get_document(
        self, dataset_id: str, document_id: str, stage: Stage = Stage.DOCUMENTS
    ) -> Optional[Document]:
        """
        Get a specific document from a dataset.

        Args:
            dataset_id: Dataset ID.
            document_id: Document ID.
            stage: Stage to get the document from.

        Returns:
            Document object or None if not found.
        """
        # Format key based on stage and ensure proper extension
        # Ensure proper extension for each stage
        stage_prefix = f"{stage.value}/{dataset_id}/"

        if stage == Stage.DOCUMENTS or stage == Stage.REPRESENTATIONS:
            key = f"{stage_prefix}{document_id}"
            if not key.endswith(".json"):
                key += ".json"
        elif stage == Stage.PARQUET:
            key = f"{stage_prefix}{document_id}"
            # Remove .json extension if present for parquet stage
            if key.endswith(".json"):
                key = key[:-5]
        else:
            raise ValueError(f"Invalid stage: {stage}")

        # Create document object
        doc = Document(self, dataset_id, key, self.bucket)

        # Check if document exists
        if not doc.exists_in_stage(stage):
            logger.warning(
                "Document %s not found in %s stage", document_id, stage.value
            )
            return None

        return doc

    def iter_documents(
        self,
        dataset_id: str,
        stage: Stage = Stage.DOCUMENTS,
        key_prefix: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Generator[str, None, None]:
        """
        Iterate over document IDs in a dataset.

        Args:
            dataset_id: Dataset ID.
            stage: Stage to list documents from.
            key_prefix: Optional key prefix to filter objects.
            limit: Optional maximum number of documents to return.

        Yields:
            Document IDs as they are discovered.
        """
        prefix = get_stage_prefix(stage, dataset_id)

        # Add key_prefix if specified
        if key_prefix:
            clean_prefix = key_prefix.strip("/")
            if clean_prefix:
                prefix = f"{prefix}{clean_prefix}/"

        # Keep track of how many we've yielded
        count = 0

        # Iterate over keys and yield document IDs
        for key in iter_prefix(self.s3_client, self.bucket, prefix):
            # Extract document ID from key - preserve the full path after dataset_id
            parts = key.split(f"{stage.value}/{dataset_id}/")
            if len(parts) > 1 and parts[1]:  # There's content after dataset_id
                doc_id = parts[1]
                # Remove extension if present
                if doc_id.endswith(".json"):
                    doc_id = doc_id[:-5]
                yield doc_id

                # Increment count and check if we've reached the limit
                count += 1
                if limit is not None and count >= limit:
                    break

    def list_documents(
        self,
        dataset_id: str,
        stage: Stage = Stage.DOCUMENTS,
        key_prefix: Optional[str] = None,
    ) -> List[str]:
        """
        List all documents in a dataset at a specific stage.

        Note: This loads all document IDs into memory. For large datasets,
        consider using iter_documents() instead.

        Args:
            dataset_id: Dataset ID.
            stage: Stage to list documents from.
            key_prefix: Optional key prefix to filter objects.

        Returns:
            List of document IDs.
        """
        return list(self.iter_documents(dataset_id, stage, key_prefix))

    def get_dataset_index(self, dataset_id: str, key_prefix: Optional[str] = None):
        """
        Get the index for a dataset.

        Args:
            dataset_id: Dataset ID.
            key_prefix: Optional key prefix that was used when building the index.

        Returns:
            The dataset index, or None if not found.
        """
        return get_dataset_index(self.s3_client, self.bucket, dataset_id, key_prefix)

    def iter_jsonl_export(
        self,
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
        Iterate over documents in a dataset for export to JSONL format.

        This streaming approach is memory-efficient for large datasets.

        Args:
            dataset_id: Dataset ID.
            source_stage: Source stage to export from (REPRESENTATIONS or PARQUET).
            key_prefix: Optional key prefix to filter objects.
            max_documents: Maximum number of documents to export.
            tokenizer: Tokenizer to extract tokens for.
            representation: Representation MIME type.
            deduplicate: Whether to deduplicate documents.
            include_metrics: Whether to include detailed metrics in the output.

        Yields:
            Processed documents ready for JSONL export.
        """
        from kl3m_data_client.operations.export import iter_jsonl_export

        return iter_jsonl_export(
            self.s3_client,
            self.bucket,
            dataset_id,
            source_stage,
            key_prefix,
            max_documents,
            tokenizer,
            representation,
            deduplicate,
            include_metrics,
        )

    def export_to_jsonl(
        self,
        dataset_id: str,
        output_path: str,
        key_prefix: Optional[str] = None,
        source_stage: Stage = Stage.PARQUET,
        max_documents: Optional[int] = None,
        tokenizer: str = "cl100k_base",
        representation: str = "text/plain",
        deduplicate: bool = True,
        include_metrics: bool = False,
    ) -> int:
        """
        Export dataset to JSONL format.

        Args:
            dataset_id: Dataset ID.
            output_path: Path to output JSONL file.
            key_prefix: Optional key prefix to filter objects.
            source_stage: Source stage to export from (REPRESENTATIONS or PARQUET).
            max_documents: Maximum number of documents to export.
            tokenizer: Tokenizer to extract tokens for.
            representation: Representation MIME type.
            deduplicate: Whether to deduplicate documents.
            include_metrics: Whether to include detailed metrics in the output.

        Returns:
            Number of documents exported.
        """

        return export_to_jsonl(
            self.s3_client,
            self.bucket,
            dataset_id,
            output_path,
            source_stage,
            key_prefix,
            max_documents,
            tokenizer,
            representation,
            deduplicate,
            include_metrics,
        )
