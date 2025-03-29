"""
Tests for the KL3M data client using mocked S3 responses.
These tests allow running without actual AWS credentials.
"""

from unittest.mock import patch
from kl3m_data_client.models.common import Stage
from kl3m_data_client.models.document import DocumentContent, RepresentationList
from tests.conftest import (
    configure_mock_list_datasets,
    configure_mock_get_document,
)


def test_mock_list_datasets(mock_client, mock_s3_client):
    """Test listing datasets with mocked responses."""
    _, stubber = mock_s3_client

    # Configure mock responses for dataset listing
    datasets = {
        "test-dataset-1": {
            Stage.DOCUMENTS: True,
            Stage.REPRESENTATIONS: True,
            Stage.PARQUET: False,
        },
        "test-dataset-2": {
            Stage.DOCUMENTS: True,
            Stage.REPRESENTATIONS: False,
            Stage.PARQUET: False,
        },
        "test-dataset-3": {
            Stage.DOCUMENTS: True,
            Stage.REPRESENTATIONS: True,
            Stage.PARQUET: True,
        },
    }

    configure_mock_list_datasets(stubber, datasets)

    # Call the method and check results
    result = mock_client.list_datasets()

    assert len(result) == 3
    assert result["test-dataset-1"][Stage.DOCUMENTS] is True
    assert result["test-dataset-1"][Stage.REPRESENTATIONS] is True
    assert result["test-dataset-1"][Stage.PARQUET] is False
    assert result["test-dataset-2"][Stage.DOCUMENTS] is True
    assert result["test-dataset-2"][Stage.REPRESENTATIONS] is False
    assert result["test-dataset-2"][Stage.PARQUET] is False
    assert result["test-dataset-3"][Stage.DOCUMENTS] is True
    assert result["test-dataset-3"][Stage.REPRESENTATIONS] is True
    assert result["test-dataset-3"][Stage.PARQUET] is True


def test_mock_iter_documents(mock_client, mock_s3_client):
    """Test document iteration with mocked responses."""
    s3_client, _ = mock_s3_client
    dataset_id = "test-dataset"
    doc_ids = ["doc-001", "doc-002", "doc-003"]

    # Mock the s3_client's methods directly
    with patch.object(s3_client, "get_paginator") as mock_paginator:
        # Set up the paginator mock
        mock_paginate = mock_paginator.return_value.paginate
        mock_paginate.return_value = [
            {
                "Contents": [
                    {"Key": f"documents/{dataset_id}/{doc_id}.json"}
                    for doc_id in doc_ids
                ]
            }
        ]

        # Call the method and check results
        result = list(mock_client.iter_documents(dataset_id, Stage.DOCUMENTS))

        assert len(result) == 3
        assert "doc-001" in result
        assert "doc-002" in result
        assert "doc-003" in result


def test_mock_get_document_content(mock_client, mock_s3_client, sample_document_data):
    """Test getting document content with mocked responses."""
    _, stubber = mock_s3_client

    dataset_id = "test-dataset"
    doc_id = "doc-001"

    # First we need to patch the decompression function to handle our test data
    with patch("kl3m_data_client.document.decompress_content", side_effect=lambda x, binary=False: x):
        # Configure mock response for document retrieval
        configure_mock_get_document(
            stubber, dataset_id, doc_id, Stage.DOCUMENTS, sample_document_data
        )

        # Call the method and check results
        document = mock_client.get_document(dataset_id, doc_id, Stage.DOCUMENTS)
        assert document is not None

        content = document.get_content(Stage.DOCUMENTS)
        assert content is not None
        assert isinstance(content, DocumentContent)
        assert content.metadata.identifier == "test-doc-001"
        assert content.metadata.source == "test-source"
        assert content.metadata.title == "Test Document"
        assert content.metadata.format == "text/plain"
        assert content.content == "This is a test document content."


def test_mock_get_document_representation(
    mock_client, mock_s3_client, sample_representation_data
):
    """Test getting document representations with mocked responses."""
    _, stubber = mock_s3_client

    dataset_id = "test-dataset"
    doc_id = "doc-001"

    # First we need to patch the decompression function to handle our test data
    with patch("kl3m_data_client.document.decompress_content", side_effect=lambda x, binary=False: x):
        # Configure mock response for representation retrieval
        configure_mock_get_document(
            stubber,
            dataset_id,
            doc_id,
            Stage.REPRESENTATIONS,
            sample_representation_data,
        )

        # Call the method and check results
        document = mock_client.get_document(dataset_id, doc_id, Stage.REPRESENTATIONS)
        assert document is not None

        # Test using get_representation
        representation = document.get_representation()
        assert representation is not None
        assert isinstance(representation, RepresentationList)
        assert representation.document_id == "test-doc-001"
        assert representation.source == "test-source"
        assert len(representation.representations) == 2
        assert "text/plain" in representation.representations
        assert "text/markdown" in representation.representations

        # Test representation content
        # Use get_content from proper representation
        plain_content = representation.get_content("text/plain")
        assert plain_content == "This is plain text content."

        markdown_content = representation.get_content("text/markdown")
        assert markdown_content == "# This is markdown content"

        # Test tokenizers
        tokenizers = representation.get_available_tokenizers("text/plain")
        assert "cl100k_base" in tokenizers

        token_count = representation.token_count("text/plain", "cl100k_base")
        assert token_count == 6

        # Test mime types
        mime_types = representation.get_available_mime_types()
        assert "text/plain" in mime_types
        assert "text/markdown" in mime_types


def test_mock_get_document_parquet(mock_client, mock_s3_client, sample_parquet_data):
    """Test getting document parquet data with mocked responses."""
    _, stubber = mock_s3_client

    dataset_id = "test-dataset"
    doc_id = "doc-001"

    # Configure mock response for parquet retrieval
    configure_mock_get_document(
        stubber, dataset_id, doc_id, Stage.PARQUET, sample_parquet_data
    )

    # Call the method and check results
    document = mock_client.get_document(dataset_id, doc_id, Stage.PARQUET)
    assert document is not None

    # Test using get_parquet
    parquet_content = document.get_parquet()
    assert parquet_content is not None
    assert parquet_content.document_id == "doc-001"
    assert parquet_content.size > 0

    # Since we're using a real parquet file from create_simple_parquet,
    # we can test the table functions
    table = parquet_content.get_table()
    assert table is not None

    columns = parquet_content.get_columns()
    assert "document_id" in columns
    assert "content" in columns
    assert "tokens" in columns

    # Test document retrieval
    document_data = parquet_content.get_document()
    assert document_data is not None
