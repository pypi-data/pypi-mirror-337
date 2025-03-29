"""
Tests for the Document class in the KL3M data client.
These tests focus on the Document class functionality without requiring AWS.
"""

import json
import pytest
from unittest.mock import Mock, patch
from kl3m_data_client.models.common import Stage
from kl3m_data_client.document import Document
from kl3m_data_client.models.document import (
    DocumentContent,
    RepresentationContent,
    ParquetContent,
)


def create_mock_document():
    """Create a mock Document instance with a mocked client."""
    # Create a mock for the KL3MClient
    mock_client = Mock()
    mock_client.s3_client = Mock()
    mock_client.bucket = "test-bucket"

    # Create a Document instance with the mock client
    doc = Document(
        client=mock_client,
        dataset_id="test-dataset",
        document_key="documents/test-dataset/doc-001.json",
        bucket="test-bucket",
    )

    return doc, mock_client


def test_document_initialization():
    """Test Document initialization."""
    doc, _ = create_mock_document()

    # Check basic properties
    assert doc.dataset_id == "test-dataset"
    assert doc.bucket == "test-bucket"
    assert doc.doc_id == "doc-001"
    assert doc.doc_path == "doc-001.json"

    # Check normalized keys
    assert doc.document_key == "documents/test-dataset/doc-001.json"
    assert doc.representation_key == "representations/test-dataset/doc-001.json"
    assert doc.parquet_key == "parquet/test-dataset/doc-001"


def test_document_exists_in_stage():
    """Test checking if a document exists in a stage."""
    doc, _ = create_mock_document()

    # Patch the check_object_exists function to return True
    with patch("kl3m_data_client.document.check_object_exists", return_value=True):
        assert doc.exists_in_stage(Stage.DOCUMENTS) is True
        assert doc.exists_in_stage(Stage.REPRESENTATIONS) is True
        assert doc.exists_in_stage(Stage.PARQUET) is True

    # Patch the check_object_exists function to return False
    with patch("kl3m_data_client.document.check_object_exists", return_value=False):
        assert doc.exists_in_stage(Stage.DOCUMENTS) is False
        assert doc.exists_in_stage(Stage.REPRESENTATIONS) is False
        assert doc.exists_in_stage(Stage.PARQUET) is False

    # Test with invalid stage
    with pytest.raises(ValueError):
        doc.exists_in_stage(Stage.INDEX)


def test_get_document_content():
    """Test getting document content."""
    doc, _ = create_mock_document()

    # Create sample document data
    sample_data = {
        "identifier": "doc-001",
        "source": "test-source",
        "title": "Test Document",
        "content": "This is test content.",
    }

    # Mock get_object_bytes to return the sample data
    # Since the client tries to decompress content if present, we need to modify our approach
    with patch(
        "kl3m_data_client.document.get_object_bytes",
        return_value=json.dumps(sample_data).encode(),
    ):
        # Patch the decompress_content function to avoid decompression attempts
        with patch(
            "kl3m_data_client.document.decompress_content", side_effect=lambda x: x
        ):
            content = doc._get_document_content()

            assert content is not None
            assert isinstance(content, DocumentContent)
            assert content.metadata.identifier == "doc-001"
            assert content.metadata.source == "test-source"
            assert content.metadata.title == "Test Document"
            assert content.content == "This is test content."

    # Test when the document doesn't exist
    with patch("kl3m_data_client.document.get_object_bytes", return_value=None):
        content = doc._get_document_content()
        assert content is None


def test_get_representation_content():
    """Test getting representation content."""
    doc, _ = create_mock_document()

    # Create sample representation data
    sample_data = {
        "documents": [
            {
                "identifier": "doc-001",
                "source": "test-source",
                "representations": {
                    "text/plain": {
                        "content": "This is content.",
                        "tokens": {"cl100k_base": [1, 2, 3, 4]},
                    }
                },
            }
        ]
    }

    # Mock get_object_bytes to return the sample data
    with patch(
        "kl3m_data_client.document.get_object_bytes",
        return_value=json.dumps(sample_data).encode(),
    ):
        content = doc._get_representation_content()

        assert content is not None
        assert isinstance(content, RepresentationContent)
        assert len(content.documents) == 1
        assert content.documents[0]["identifier"] == "doc-001"
        assert content.documents[0]["source"] == "test-source"
        assert "text/plain" in content.documents[0]["representations"]

    # Test when the representations don't exist
    with patch("kl3m_data_client.document.get_object_bytes", return_value=None):
        content = doc._get_representation_content()
        assert content is None


def test_get_representation():
    """Test getting representation as a RepresentationList."""
    doc, _ = create_mock_document()

    # Create sample representation data
    sample_data = {
        "documents": [
            {
                "identifier": "doc-001",
                "source": "test-source",
                "representations": {
                    "text/plain": {
                        "content": "This is content.",
                        "tokens": {"cl100k_base": [1, 2, 3, 4]},
                    }
                },
            }
        ]
    }

    # Mock _get_representation_content to return the sample data
    with patch.object(
        doc,
        "_get_representation_content",
        return_value=RepresentationContent.from_dict(sample_data),
    ):
        rep_list = doc.get_representation()

        assert rep_list is not None
        assert rep_list.document_id == "doc-001"
        assert rep_list.source == "test-source"
        assert "text/plain" in rep_list.representations
        assert rep_list.get_content("text/plain") == "This is content."
        assert rep_list.token_count("text/plain", "cl100k_base") == 4

    # Test when representations don't exist
    with patch.object(doc, "_get_representation_content", return_value=None):
        rep_list = doc.get_representation()
        assert rep_list is None


def test_get_parquet_content():
    """Test getting parquet content."""
    doc, _ = create_mock_document()

    # Create a mock for parquet data
    from kl3m_data_client.utils.parquet_utils import create_simple_parquet

    mock_parquet_data = create_simple_parquet(
        "doc-001", "This is test content for parquet."
    )

    # Mock get_object_bytes to return the mock parquet data
    with patch(
        "kl3m_data_client.document.get_object_bytes", return_value=mock_parquet_data
    ):
        content = doc._get_parquet_content()

        assert content is not None
        assert isinstance(content, ParquetContent)
        assert content.document_id == "doc-001"
        assert content.size > 0

        # Test table operations
        table = content.get_table()
        assert table is not None
        assert "document_id" in content.get_columns()
        assert "content" in content.get_columns()

    # Test when parquet data doesn't exist
    with patch("kl3m_data_client.document.get_object_bytes", return_value=None):
        content = doc._get_parquet_content()
        assert content is None
