"""
Integration tests for the KL3M data client with AWS S3.
These tests require AWS credentials to be set up in the environment.
"""

import pytest
from kl3m_data_client.utils.s3 import (
    get_s3_client,
    check_object_exists,
    get_stage_prefix,
    list_common_prefixes,
    iter_prefix,
)
from kl3m_data_client.models.common import Stage


# Mark all tests in this file as integration tests
pytestmark = pytest.mark.integration


@pytest.fixture
def s3_client():
    """Create an S3 client for testing."""
    # This will use AWS credentials from environment variables
    return get_s3_client()


@pytest.fixture
def bucket():
    """Return the bucket to use for testing."""
    return "data.kl3m.ai"


def test_get_s3_client():
    """Test creating an S3 client."""
    client = get_s3_client()
    assert client is not None

    # Check that the client can make a basic call
    response = client.list_buckets()
    assert "Buckets" in response


def test_get_stage_prefix():
    """Test getting stage prefixes."""
    doc_prefix = get_stage_prefix(Stage.DOCUMENTS, "test-dataset")
    assert doc_prefix == "documents/test-dataset/"

    rep_prefix = get_stage_prefix(Stage.REPRESENTATIONS, "test-dataset")
    assert rep_prefix == "representations/test-dataset/"

    parquet_prefix = get_stage_prefix(Stage.PARQUET, "test-dataset")
    assert parquet_prefix == "parquet/test-dataset/"

    index_prefix = get_stage_prefix(Stage.INDEX)
    assert index_prefix == "index/"


def test_list_common_prefixes(s3_client, bucket):
    """Test listing common prefixes (folders) in S3."""
    # List the stages (documents, representations, parquet)
    prefixes = list_common_prefixes(s3_client, bucket, "")
    assert len(prefixes) > 0

    # Check that the expected prefixes are present
    stage_prefixes = [p for p in prefixes if p.rstrip("/") in [s.value for s in Stage]]
    assert len(stage_prefixes) > 0


def test_iter_prefix(s3_client, bucket):
    """Test iterating over objects with a prefix."""
    # Get the documents prefix for a known dataset (limit to first few)
    document_prefix = get_stage_prefix(Stage.DOCUMENTS, "fdlp")

    # Iterate over the first few objects
    objects = list(iter_prefix(s3_client, bucket, document_prefix, max_items=5))

    # Check that we got some objects
    assert len(objects) > 0
    assert all(obj.startswith(document_prefix) for obj in objects)


def test_check_object_exists(s3_client, bucket):
    """Test checking if an object exists."""
    # Get a document key from a known dataset
    document_prefix = get_stage_prefix(Stage.DOCUMENTS, "fdlp")

    # Get the first object key
    first_object = next(iter_prefix(s3_client, bucket, document_prefix))

    # Check that the object exists
    assert check_object_exists(s3_client, bucket, first_object)

    # Check that a non-existent object doesn't exist
    assert not check_object_exists(s3_client, bucket, "non-existent-key")
