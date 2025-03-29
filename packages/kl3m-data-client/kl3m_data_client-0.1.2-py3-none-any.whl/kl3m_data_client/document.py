"""
Document class for interacting with documents in the KL3M data pipeline.
"""

import json
import logging
from typing import Optional, Any, Union

from kl3m_data_client.models.common import Stage
from kl3m_data_client.models.document import (
    DocumentContent,
    RepresentationContent,
    RepresentationList,
    ParquetContent,
)
from kl3m_data_client.utils.s3 import (
    get_object_bytes,
    check_object_exists,
    decompress_content,
)

logger = logging.getLogger("kl3m_data_client")


class Document:
    """
    Representation of a document in the KL3M pipeline.
    """

    def __init__(
        self,
        client: Any,
        dataset_id: str,
        document_key: str,
        bucket: str = "data.kl3m.ai",
    ):
        """
        Initialize a document representation.

        Args:
            client: The KL3MClient instance.
            dataset_id: The dataset ID.
            document_key: The document key (can be from any stage).
            bucket: The S3 bucket name.
        """
        self.client = client
        self.dataset_id = dataset_id
        self.bucket = bucket
        self.s3_client = client.s3_client

        # Extract the document identifier from the key (last part of the path)
        path_parts = document_key.split("/")
        self.doc_id = (
            path_parts[-1].split(".")[0] if len(path_parts) > 1 else document_key
        )

        # Extract the document path after stage and dataset_id
        # This will include any key_prefix and the document name
        stage_and_dataset = False
        for stage in [
            Stage.DOCUMENTS.value,
            Stage.REPRESENTATIONS.value,
            Stage.PARQUET.value,
        ]:
            stage_dataset_prefix = f"{stage}/{dataset_id}/"
            if document_key.startswith(stage_dataset_prefix):
                # Extract everything after stage/dataset_id/
                self.doc_path = document_key[len(stage_dataset_prefix) :]
                stage_and_dataset = True
                break

        if not stage_and_dataset:
            # If we couldn't extract from a known stage, use the full key
            self.doc_path = document_key

        # Normalize keys for all stages using the document path
        # Combination of stage + dataset_id + doc_path
        self.document_key = f"{Stage.DOCUMENTS.value}/{dataset_id}/{self.doc_path}"
        self.representation_key = (
            f"{Stage.REPRESENTATIONS.value}/{dataset_id}/{self.doc_path}"
        )

        # For parquet key, remove .json extension if present
        if self.doc_path.endswith(".json"):
            parquet_doc_path = self.doc_path[:-5]  # Remove .json
        else:
            parquet_doc_path = self.doc_path

        self.parquet_key = f"{Stage.PARQUET.value}/{dataset_id}/{parquet_doc_path}"

        logger.debug(
            "Document keys initialized: %s, %s, %s",
            self.document_key,
            self.representation_key,
            self.parquet_key,
        )

    def exists_in_stage(self, stage: Stage) -> bool:
        """
        Check if the document exists in a specific stage.

        Args:
            stage: The stage to check.

        Returns:
            Whether the document exists in the stage.
        """
        # Use the appropriate key for the stage
        if stage == Stage.DOCUMENTS:
            key_to_check = self.document_key
        elif stage == Stage.REPRESENTATIONS:
            key_to_check = self.representation_key
        elif stage == Stage.PARQUET:
            key_to_check = self.parquet_key
        else:
            raise ValueError(f"Invalid stage: {stage}")

        # Check if the object exists
        return check_object_exists(self.s3_client, self.bucket, key_to_check)

    def get_content(
        self, stage: Stage = Stage.DOCUMENTS
    ) -> Optional[Union[DocumentContent, RepresentationContent, ParquetContent]]:
        """
        Get the document content from a specific stage.

        Args:
            stage: The stage to get content from.

        Returns:
            The document content, or None if not found.

        Note:
            - For Stage.DOCUMENTS, returns DocumentContent
            - For Stage.REPRESENTATIONS, returns RepresentationContent
            - For Stage.PARQUET, returns ParquetContent
        """
        # Return appropriate content based on stage
        if stage == Stage.DOCUMENTS:
            return self._get_document_content()
        elif stage == Stage.REPRESENTATIONS:
            return self._get_representation_content()
        elif stage == Stage.PARQUET:
            return self._get_parquet_content()
        else:
            raise ValueError(f"Invalid stage: {stage}")

    def get_document_content(self) -> Optional[DocumentContent]:
        """Convenience method to get typed document content."""
        return self._get_document_content()

    def get_representation_content(self) -> Optional[RepresentationContent]:
        """Convenience method to get typed representation content."""
        return self._get_representation_content()

    def _get_document_content(self) -> Optional[DocumentContent]:
        """
        Get the document content from the Documents stage.

        Returns:
            The document content, or None if not found.
        """
        # Get document bytes
        doc_bytes = get_object_bytes(self.s3_client, self.bucket, self.document_key)
        if not doc_bytes:
            return None

        # Parse document data
        try:
            data = json.loads(doc_bytes)

            # Handle compressed content if needed
            if isinstance(data.get("content"), str) and "content" in data:
                data["content"] = decompress_content(data["content"])

            return DocumentContent.from_dict(data)
        except Exception as e:
            logger.error("Error parsing document data: %s", e)
            return None

    def _get_representation_content(self) -> Optional[RepresentationContent]:
        """
        Get the representation content from the Representations stage.

        Returns:
            The representation content, or None if not found.
        """
        # Get representation bytes
        rep_bytes = get_object_bytes(
            self.s3_client, self.bucket, self.representation_key
        )
        if not rep_bytes:
            return None

        # Parse representation data
        try:
            data = json.loads(rep_bytes)

            # Handle compressed content in each representation
            if "documents" in data:
                for doc in data["documents"]:
                    if "representations" in doc:
                        for _, rep in doc[
                            "representations"
                        ].items():  # Using _ for unused variable
                            if isinstance(rep.get("content"), str) and "content" in rep:
                                rep["content"] = decompress_content(rep["content"])

            return RepresentationContent.from_dict(data)
        except Exception as e:
            logger.error("Error parsing representation data: %s", e)
            return None

    def get_representation(self) -> Optional[RepresentationList]:
        """
        Get the document representations as a more accessible RepresentationList object.

        This provides a more convenient way to access representation data compared
        to using get_content(Stage.REPRESENTATIONS) directly.

        Returns:
            A RepresentationList object, or None if not found.
        """
        rep_content = self._get_representation_content()
        if not rep_content:
            return None

        return rep_content.get_representation(0)

    def get_parquet(self) -> Optional[ParquetContent]:
        """
        Get the parquet data as a ParquetContent object.

        This provides a more convenient way to access parquet data compared
        to using get_content(Stage.PARQUET) directly.

        Returns:
            A ParquetContent object, or None if not found.
        """
        return self._get_parquet_content()

    def _get_parquet_content(self) -> Optional[ParquetContent]:
        """
        Get the parquet content from the Parquet stage.

        Returns:
            The parquet data wrapped in a ParquetContent object, or None if not found.
        """
        data = get_object_bytes(self.s3_client, self.bucket, self.parquet_key)
        if not data:
            return None

        # Extract document ID from the key
        parts = self.parquet_key.split("/")
        doc_id = parts[-1] if parts else self.doc_id

        return ParquetContent.from_bytes(doc_id, data)

    def process_to_representations(self) -> bool:
        """
        Process the document to the Representations stage.

        Returns:
            Whether the processing was successful.
        """
        # Delegate to the client for processing
        return self.client.process_document_to_representations(self)

    def process_to_parquet(self) -> bool:
        """
        Process the document to the Parquet stage.

        Returns:
            Whether the processing was successful.
        """
        # Delegate to the client for processing
        return self.client.process_document_to_parquet(self)
