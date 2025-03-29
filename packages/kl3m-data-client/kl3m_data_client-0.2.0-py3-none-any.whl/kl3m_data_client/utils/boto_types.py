"""
Type definitions for boto3 clients to improve mypy compatibility.
"""

from typing import Any, Dict, Union, Protocol


# Define a type for the S3 client
class S3Client(Protocol):
    """Protocol type for boto3 S3 client to improve mypy compatibility."""

    def list_objects_v2(self, **kwargs: Any) -> Dict[str, Any]:
        """List objects V2 operation in S3."""
        ...

    def list_objects(self, **kwargs: Any) -> Dict[str, Any]:
        """List objects operation in S3."""
        ...

    def get_object(self, **kwargs: Any) -> Dict[str, Any]:
        """Get object operation in S3."""
        ...

    def put_object(self, **kwargs: Any) -> Dict[str, Any]:
        """Put object operation in S3."""
        ...

    def head_object(self, **kwargs: Any) -> Dict[str, Any]:
        """Head object operation in S3."""
        ...

    def get_paginator(self, operation_name: str) -> Any:
        """Get paginator for S3 operations."""
        ...

    @property
    def exceptions(self) -> Any:
        """Access S3 client exceptions."""
        ...


# Type alias for boto3 client
S3ClientType = Union[S3Client, Any]
