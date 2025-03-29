"""
Tests for the model classes in the KL3M data client.
These tests focus on the functionality of the models without requiring AWS access.
"""

from datetime import datetime
from kl3m_data_client.models.common import Stage, DatasetStatus, ProcessingResult
from kl3m_data_client.models.document import (
    DocumentMetadata,
    DocumentContent,
    SingleRepresentation,
    RepresentationList,
    RepresentationContent,
)
from kl3m_data_client.models.stage import IndexMetadata, DatasetIndex


def test_stage_enum():
    """Test the Stage enum."""
    assert Stage.DOCUMENTS.value == "documents"
    assert Stage.REPRESENTATIONS.value == "representations"
    assert Stage.PARQUET.value == "parquet"
    assert Stage.INDEX.value == "index"


def test_dataset_status():
    """Test the DatasetStatus class."""
    status = DatasetStatus(
        dataset_id="test",
        document_count=100,
        representation_count=80,
        parquet_count=70,
        missing_representations=20,
        missing_parquet=10,
    )

    # Test properties
    assert status.dataset_id == "test"
    assert status.document_count == 100
    assert status.representation_count == 80
    assert status.parquet_count == 70
    assert status.missing_representations == 20
    assert status.missing_parquet == 10
    assert status.is_complete is False
    assert status.total_documents == 100

    # Test as_dict method
    status_dict = status.as_dict()
    assert status_dict["dataset_id"] == "test"
    assert status_dict["document_count"] == 100
    assert status_dict["representation_count"] == 80
    assert status_dict["parquet_count"] == 70
    assert status_dict["missing_representations"] == 20
    assert status_dict["missing_parquet"] == 10
    assert status_dict["is_complete"] is False

    # Test completed status
    completed_status = DatasetStatus(
        dataset_id="test",
        document_count=100,
        representation_count=100,
        parquet_count=100,
        missing_representations=0,
        missing_parquet=0,
    )
    assert completed_status.is_complete is True


def test_processing_result():
    """Test the ProcessingResult class."""
    result = ProcessingResult(processed_count=90, error_count=10, duration_seconds=5.0)

    # Test properties
    assert result.processed_count == 90
    assert result.error_count == 10
    assert result.duration_seconds == 5.0
    assert result.total_count == 100
    assert result.success_rate == 90.0
    assert result.docs_per_second == 18.0

    # Test edge cases
    empty_result = ProcessingResult(
        processed_count=0, error_count=0, duration_seconds=0
    )
    assert empty_result.success_rate == 100.0
    assert empty_result.docs_per_second == 0.0


def test_document_metadata():
    """Test the DocumentMetadata class."""
    # Test creation
    metadata = DocumentMetadata(
        identifier="doc1",
        source="test_source",
        title="Test Document",
        date="2023-01-01",
        format="text/plain",
        language="en",
    )

    assert metadata.identifier == "doc1"
    assert metadata.source == "test_source"
    assert metadata.title == "Test Document"
    assert metadata.date == "2023-01-01"
    assert metadata.format == "text/plain"
    assert metadata.language == "en"

    # Test from_dict method
    metadata_dict = {
        "identifier": "doc2",
        "source": "another_source",
        "title": "Another Document",
        "format": "text/html",
    }
    metadata_from_dict = DocumentMetadata.from_dict(metadata_dict)

    assert metadata_from_dict.identifier == "doc2"
    assert metadata_from_dict.source == "another_source"
    assert metadata_from_dict.title == "Another Document"
    assert metadata_from_dict.format == "text/html"
    assert metadata_from_dict.date is None
    assert metadata_from_dict.language is None


def test_document_content():
    """Test the DocumentContent class."""
    metadata = DocumentMetadata(
        identifier="doc1", source="test_source", title="Test Document"
    )

    content = DocumentContent(content="This is test content.", metadata=metadata)

    assert content.content == "This is test content."
    assert content.metadata.identifier == "doc1"
    assert content.metadata.source == "test_source"

    # Test from_dict method
    content_dict = {
        "content": "Another test content.",
        "identifier": "doc2",
        "source": "another_source",
        "title": "Another Document",
    }
    content_from_dict = DocumentContent.from_dict(content_dict)

    assert content_from_dict.content == "Another test content."
    assert content_from_dict.metadata.identifier == "doc2"
    assert content_from_dict.metadata.source == "another_source"


def test_single_representation():
    """Test the SingleRepresentation class."""
    rep = SingleRepresentation(
        mime_type="text/plain",
        content="This is a test content.",
        tokens={"cl100k_base": [123, 456, 789]},
    )

    assert rep.mime_type == "text/plain"
    assert rep.content == "This is a test content."
    assert rep.tokens == {"cl100k_base": [123, 456, 789]}

    # Test token methods
    assert rep.get_tokens("cl100k_base") == [123, 456, 789]
    assert rep.get_tokens("non_existent") is None
    assert rep.get_available_tokenizers() == ["cl100k_base"]
    assert rep.token_count("cl100k_base") == 3
    assert rep.token_count("non_existent") == 0

    # Test from_dict method
    rep_dict = {
        "content": "Another test content.",
        "tokens": {
            "cl100k_base": [111, 222, 333, 444],
            "another_tokenizer": [555, 666, 777],
        },
    }
    rep_from_dict = SingleRepresentation.from_dict("text/markdown", rep_dict)

    assert rep_from_dict.mime_type == "text/markdown"
    assert rep_from_dict.content == "Another test content."
    assert rep_from_dict.tokens["cl100k_base"] == [111, 222, 333, 444]
    assert rep_from_dict.tokens["another_tokenizer"] == [555, 666, 777]
    assert rep_from_dict.get_available_tokenizers() == [
        "cl100k_base",
        "another_tokenizer",
    ]
    assert rep_from_dict.token_count("cl100k_base") == 4
    assert rep_from_dict.token_count("another_tokenizer") == 3

    # Test string representation
    assert "text/plain" in str(rep)
    assert "content" in str(rep)
    assert "cl100k_base: 3 tokens" in str(rep)


def test_representation_list():
    """Test the RepresentationList class."""
    # Create representations
    plain_rep = SingleRepresentation(
        mime_type="text/plain",
        content="Plain text content",
        tokens={"cl100k_base": [1, 2, 3, 4]},
    )

    markdown_rep = SingleRepresentation(
        mime_type="text/markdown",
        content="# Markdown content",
        tokens={"cl100k_base": [5, 6, 7]},
    )

    # Create representation list
    rep_list = RepresentationList(
        document_id="doc1",
        source="test_source",
        metadata={"title": "Test Document"},
        representations={"text/plain": plain_rep, "text/markdown": markdown_rep},
    )

    # Test basic properties
    assert rep_list.document_id == "doc1"
    assert rep_list.source == "test_source"
    assert rep_list.metadata["title"] == "Test Document"
    assert len(rep_list.representations) == 2
    assert rep_list.success is True
    assert rep_list.error is None

    # Test helper methods
    assert rep_list.get_representation("text/plain") == plain_rep
    assert rep_list.get_representation("text/html") is None
    assert rep_list.get_content("text/plain") == "Plain text content"
    assert rep_list.get_content("text/html") is None
    assert rep_list.get_tokens("text/plain", "cl100k_base") == [1, 2, 3, 4]
    assert rep_list.get_tokens("text/html", "cl100k_base") is None
    assert set(rep_list.get_available_mime_types()) == {"text/plain", "text/markdown"}
    assert set(rep_list.get_available_tokenizers("text/plain")) == {"cl100k_base"}
    assert rep_list.token_count("text/plain", "cl100k_base") == 4
    assert rep_list.token_count("text/markdown", "cl100k_base") == 3
    assert rep_list.token_count("text/html", "cl100k_base") == 0

    # Test from_document_data method
    doc_data = {
        "identifier": "doc2",
        "source": "another_source",
        "metadata": {"title": "Another Document"},
        "representations": {
            "text/plain": {
                "content": "More text content",
                "tokens": {"cl100k_base": [10, 20, 30, 40, 50]},
            },
            "text/html": {
                "content": "<html><body>HTML content</body></html>",
                "tokens": {"cl100k_base": [60, 70, 80]},
            },
        },
    }
    rep_list_from_data = RepresentationList.from_document_data(doc_data)

    assert rep_list_from_data.document_id == "doc2"
    assert rep_list_from_data.source == "another_source"
    assert rep_list_from_data.metadata["title"] == "Another Document"
    assert len(rep_list_from_data.representations) == 2
    assert rep_list_from_data.get_content("text/plain") == "More text content"
    assert rep_list_from_data.token_count("text/html", "cl100k_base") == 3

    # Test summarize method
    summary = rep_list.summarize()
    assert summary["document_id"] == "doc1"
    assert summary["source"] == "test_source"
    assert set(summary["mime_types"]) == {"text/plain", "text/markdown"}
    assert summary["token_counts"]["text/plain"]["cl100k_base"] == 4


def test_representation_content():
    """Test the RepresentationContent class."""
    # Create test document data
    doc_data = {
        "documents": [
            {
                "identifier": "doc1",
                "source": "test_source",
                "representations": {
                    "text/plain": {
                        "content": "Plain text content",
                        "tokens": {"cl100k_base": [1, 2, 3, 4]},
                    }
                },
            },
            {
                "identifier": "doc2",
                "source": "another_source",
                "representations": {
                    "text/markdown": {
                        "content": "# Markdown",
                        "tokens": {"cl100k_base": [5, 6, 7]},
                    }
                },
            },
        ]
    }

    # Create representation content
    rep_content = RepresentationContent.from_dict(doc_data)

    # Test basic properties
    assert len(rep_content.documents) == 2
    assert rep_content.documents[0]["identifier"] == "doc1"
    assert rep_content.documents[1]["identifier"] == "doc2"

    # Test helper methods
    assert rep_content.get_document_data(0)["identifier"] == "doc1"
    assert rep_content.get_document_data(2) is None

    rep_list = rep_content.get_representation(0)
    assert rep_list is not None
    assert rep_list.document_id == "doc1"
    assert rep_list.source == "test_source"

    assert rep_content.get_text_content("text/plain", 0) == "Plain text content"
    assert rep_content.get_text_content("text/markdown", 0) is None
    assert rep_content.get_text_content("text/plain", 2) is None

    assert rep_content.get_tokens("cl100k_base", "text/plain", 0) == [1, 2, 3, 4]
    assert rep_content.get_tokens("cl100k_base", "text/markdown", 0) is None

    all_reps = rep_content.get_all_representations()
    assert len(all_reps) == 2
    assert all_reps[0].document_id == "doc1"
    assert all_reps[1].document_id == "doc2"

    # Test string representation
    assert "RepresentationContent" in str(rep_content)
    assert "2 documents" in str(rep_content)

    # Test empty case
    empty_content = RepresentationContent.from_dict({"documents": []})
    assert "empty" in str(empty_content)


def test_index_metadata():
    """Test the IndexMetadata class."""
    now = datetime.now()

    # Create index metadata
    metadata = IndexMetadata(
        dataset_id="test_dataset", key_prefix="test/", count=100, created_at=now
    )

    # Test properties
    assert metadata.dataset_id == "test_dataset"
    assert metadata.key_prefix == "test/"
    assert metadata.count == 100
    assert metadata.created_at == now

    # Test from_dict method
    metadata_dict = {
        "dataset_id": "another_dataset",
        "key_prefix": "another/",
        "count": 200,
        "created_at": now.isoformat(),
    }
    metadata_from_dict = IndexMetadata.from_dict(metadata_dict)

    assert metadata_from_dict.dataset_id == "another_dataset"
    assert metadata_from_dict.key_prefix == "another/"
    assert metadata_from_dict.count == 200
    assert isinstance(metadata_from_dict.created_at, datetime)

    # Test default created_at
    default_metadata = IndexMetadata.from_dict({"dataset_id": "default"})
    assert default_metadata.dataset_id == "default"
    assert default_metadata.key_prefix is None
    assert default_metadata.count == 0
    assert isinstance(default_metadata.created_at, datetime)


def test_dataset_index():
    """Test the DatasetIndex class."""
    # Create index metadata
    metadata = IndexMetadata(
        dataset_id="test_dataset",
        key_prefix="test/",
        count=3,
        created_at=datetime.now(),
    )

    # Create dataset index
    objects = [
        "documents/test_dataset/doc1.json",
        "documents/test_dataset/doc2.json",
        "documents/test_dataset/subdir/doc3.json",
    ]
    index = DatasetIndex(objects=objects, metadata=metadata)

    # Test properties
    assert index.objects == objects
    assert index.metadata.dataset_id == "test_dataset"
    assert index.metadata.count == 3

    # Test get_document_ids method
    doc_ids = index.get_document_ids()
    assert doc_ids == {"doc1", "doc2", "doc3"}

    # Test from_dict method
    index_dict = {
        "objects": [
            "documents/another_dataset/doc4.json",
            "documents/another_dataset/doc5.json",
        ],
        "metadata": {"dataset_id": "another_dataset", "count": 2},
    }
    index_from_dict = DatasetIndex.from_dict(index_dict)

    assert len(index_from_dict.objects) == 2
    assert index_from_dict.metadata.dataset_id == "another_dataset"
    assert index_from_dict.metadata.count == 2
    assert index_from_dict.get_document_ids() == {"doc4", "doc5"}
