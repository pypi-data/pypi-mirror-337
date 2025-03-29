"""
Pytest configuration file for KL3M data client tests.
This sets up fixtures for testing, including a mock S3 client.
"""

import json
import pytest
import boto3
from botocore.stub import Stubber
from unittest.mock import MagicMock
from kl3m_data_client import KL3MClient
from kl3m_data_client.models.common import Stage
from kl3m_data_client.utils.parquet_utils import create_simple_parquet


@pytest.fixture
def mock_s3_client():
    """Create a mocked S3 client."""
    s3_client = boto3.client("s3", region_name="us-east-1")
    stubber = Stubber(s3_client)

    # Configure stubber responses for basic operations here if needed

    stubber.activate()
    return s3_client, stubber


@pytest.fixture
def mock_client(mock_s3_client):
    """Create a KL3M client with a mocked S3 client."""
    s3_client, _ = mock_s3_client
    client = KL3MClient(s3_client=s3_client, verbose=False)
    return client


@pytest.fixture
def sample_document_data():
    """Sample document data for testing."""
    return {
        "identifier": "test-doc-001",
        "source": "test-source",
        "title": "Test Document",
        "format": "text/plain",
        "language": "en",
        "content": "This is a test document content.",
    }


@pytest.fixture
def sample_representation_data():
    """Sample representation data for testing."""
    return {
        "documents": [
            {
                "identifier": "test-doc-001",
                "source": "test-source",
                "representations": {
                    "text/plain": {
                        "content": "This is plain text content.",
                        "tokens": {"cl100k_base": [1, 2, 3, 4, 5, 6]},
                    },
                    "text/markdown": {
                        "content": "# This is markdown content",
                        "tokens": {"cl100k_base": [7, 8, 9, 10, 11]},
                    },
                },
            }
        ]
    }


@pytest.fixture
def sample_parquet_data():
    """Sample parquet data for testing."""
    return create_simple_parquet(
        document_id="test-doc-001", text="This is a test document content for parquet."
    )


def configure_mock_list_datasets(stubber, datasets):
    """Configure the stubber to respond to list_objects_v2 calls for datasets."""
    # Mock for documents stage
    prefixes = []
    for dataset_id, stages in datasets.items():
        if stages.get(Stage.DOCUMENTS, False):
            prefixes.append({"Prefix": f"{Stage.DOCUMENTS.value}/{dataset_id}/"})

    stubber.add_response(
        "list_objects_v2",
        {"CommonPrefixes": prefixes},
        {
            "Bucket": "data.kl3m.ai",
            "Prefix": f"{Stage.DOCUMENTS.value}/",
            "Delimiter": "/",
        },
    )

    # Mock for representations stage
    prefixes = []
    for dataset_id, stages in datasets.items():
        if stages.get(Stage.REPRESENTATIONS, False):
            prefixes.append({"Prefix": f"{Stage.REPRESENTATIONS.value}/{dataset_id}/"})

    stubber.add_response(
        "list_objects_v2",
        {"CommonPrefixes": prefixes},
        {
            "Bucket": "data.kl3m.ai",
            "Prefix": f"{Stage.REPRESENTATIONS.value}/",
            "Delimiter": "/",
        },
    )

    # Mock for parquet stage
    prefixes = []
    for dataset_id, stages in datasets.items():
        if stages.get(Stage.PARQUET, False):
            prefixes.append({"Prefix": f"{Stage.PARQUET.value}/{dataset_id}/"})

    stubber.add_response(
        "list_objects_v2",
        {"CommonPrefixes": prefixes},
        {
            "Bucket": "data.kl3m.ai",
            "Prefix": f"{Stage.PARQUET.value}/",
            "Delimiter": "/",
        },
    )


def configure_mock_iter_documents(stubber, dataset_id, stage, doc_ids):
    """Configure the stubber to respond to list_objects_v2 calls for document iteration."""
    contents = []
    for doc_id in doc_ids:
        key = f"{stage.value}/{dataset_id}/{doc_id}"
        if stage in [Stage.DOCUMENTS, Stage.REPRESENTATIONS]:
            key += ".json"
        contents.append({"Key": key})

    # Our implementation uses a paginator,
    # so we need to mock the paginator operation instead of list_objects_v2
    stubber.add_response(
        method="get_paginator",
        service_response={"paginator": "list_objects_v2"},
        expected_params={"operation_name": "list_objects_v2"},
    )

    # Mock the paginate response to return our contents
    stubber.add_response(
        method="paginate",
        service_response=[{"Contents": contents}],
        expected_params={
            "Bucket": "data.kl3m.ai",
            "Prefix": f"{stage.value}/{dataset_id}/",
        },
    )


def configure_mock_get_document(stubber, dataset_id, doc_id, stage, content):
    """Configure the stubber to respond to get_object calls for a document."""
    key = f"{stage.value}/{dataset_id}/{doc_id}"
    if stage in [Stage.DOCUMENTS, Stage.REPRESENTATIONS]:
        key += ".json"

    # Mock head_object to check if the document exists
    stubber.add_response("head_object", {}, {"Bucket": "data.kl3m.ai", "Key": key})

    # Mock get_object to retrieve the document content
    if isinstance(content, dict):
        body = json.dumps(content).encode("utf-8")
    else:
        body = content

    stubber.add_response(
        "get_object",
        {"Body": MagicMock(read=lambda: body)},
        {"Bucket": "data.kl3m.ai", "Key": key},
    )
