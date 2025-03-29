"""
Tests for the basic functionality of the KL3M data client.
These tests focus on the read-only operations demonstrated in examples/simple_usage.py.
They are designed to work with the actual AWS environment.
"""

import pytest
from kl3m_data_client import KL3MClient
from kl3m_data_client.models.common import Stage
from kl3m_data_client.models.document import (
    DocumentContent,
    RepresentationList,
    ParquetContent,
)


@pytest.fixture
def client():
    """Create a client for testing."""
    # We'll use environment variables for AWS credentials
    return KL3MClient(verbose=False)


@pytest.fixture
def dataset_id():
    """Return the dataset ID to use for testing."""
    # Using the same dataset as in the example
    return "usc"


def test_client_initialization():
    """Test that the client can be initialized properly."""
    client = KL3MClient(verbose=False)
    assert client is not None
    assert client.bucket == "data.kl3m.ai"
    assert client.s3_client is not None


def test_list_datasets(client):
    """Test listing available datasets."""
    datasets = client.list_datasets()
    assert isinstance(datasets, dict)
    assert len(datasets) > 0

    # Check that at least one dataset has data in the Documents stage
    assert any(stage_info[Stage.DOCUMENTS] for stage_info in datasets.values())


def test_iter_documents(client, dataset_id):
    """Test iterating over documents in a dataset."""
    # Get a small number of documents
    documents = list(client.iter_documents(dataset_id, Stage.DOCUMENTS, limit=3))

    # Check that we got some documents
    assert len(documents) > 0
    assert len(documents) <= 3

    # Check that the document IDs are strings
    for doc_id in documents:
        assert isinstance(doc_id, str)


def test_get_document(client, dataset_id):
    """Test retrieving a specific document."""
    # Get a document ID from the dataset
    doc_id = next(client.iter_documents(dataset_id, Stage.DOCUMENTS, limit=1))

    # Retrieve the document
    document = client.get_document(dataset_id, doc_id, Stage.DOCUMENTS)

    # Check that the document exists
    assert document is not None


def test_document_content(client, dataset_id):
    """Test retrieving document content."""
    # Get a document ID from the dataset
    doc_id = next(client.iter_documents(dataset_id, Stage.DOCUMENTS, limit=1))

    # Retrieve the document
    document = client.get_document(dataset_id, doc_id, Stage.DOCUMENTS)

    # Get the document content
    content = document.get_content(Stage.DOCUMENTS)

    # Check that the content exists and has the expected structure
    assert content is not None
    assert isinstance(content, DocumentContent)
    assert content.metadata is not None
    assert content.metadata.source is not None
    assert content.content is not None


def test_document_representations(client, dataset_id):
    """Test retrieving document representations."""
    # Get a document ID from the dataset
    doc_id = next(client.iter_documents(dataset_id, Stage.DOCUMENTS, limit=1))

    # Retrieve the document
    document = client.get_document(dataset_id, doc_id, Stage.DOCUMENTS)

    # Try to get representation using the improved RepresentationList interface
    representation_list = document.get_representation()

    # Check if representations exist - they might not for all documents
    if representation_list:
        assert isinstance(representation_list, RepresentationList)
        # The source might be None for some documents
        assert hasattr(representation_list, "source")

        # Check for MIME types
        mime_types = representation_list.get_available_mime_types()
        if mime_types:
            # Test getting content for a MIME type
            mime_type = mime_types[0]
            content = representation_list.get_content(mime_type)

            # Check for tokenizers if available
            tokenizers = representation_list.get_available_tokenizers(mime_type)
            if tokenizers:
                # Test token count functionality
                token_count = representation_list.token_count(mime_type, tokenizers[0])
                assert isinstance(token_count, int)


def test_document_parquet(client, dataset_id):
    """Test retrieving document parquet data."""
    # Get a document ID from the dataset
    doc_id = next(client.iter_documents(dataset_id, Stage.DOCUMENTS, limit=1))

    # Retrieve the document
    document = client.get_document(dataset_id, doc_id, Stage.DOCUMENTS)

    # Try to get parquet data
    parquet_content = document.get_parquet()

    # Check if parquet data exists - it might not for all documents
    if parquet_content:
        assert isinstance(parquet_content, ParquetContent)
        # The document_id might be different from the requested doc_id
        assert hasattr(parquet_content, "document_id")
        assert parquet_content.size > 0

        # Test PyArrow table functionality if available
        table = parquet_content.get_table()
        if table:
            assert parquet_content.get_columns() is not None
            assert len(table) > 0

            # Test representation functionality
            representations = parquet_content.get_representations()
            assert isinstance(representations, dict)


def test_dataset_status(client, dataset_id):
    """Test retrieving dataset status."""
    status = client.get_dataset_status(dataset_id)

    # Check that the status exists and has the expected structure
    assert status is not None
    assert status.dataset_id == dataset_id
    assert status.document_count >= 0
    assert status.representation_count >= 0
    assert status.parquet_count >= 0
    assert hasattr(status, "is_complete")
    assert hasattr(status, "total_documents")


def test_dataset_index(client, dataset_id):
    """Test retrieving dataset index."""
    index = client.get_dataset_index(dataset_id)

    # The index might not exist for all datasets
    if index:
        assert index.metadata is not None
        assert index.metadata.dataset_id == dataset_id
        assert index.metadata.count >= 0

        # Test document ID extraction
        doc_ids = index.get_document_ids()
        assert isinstance(doc_ids, set)
