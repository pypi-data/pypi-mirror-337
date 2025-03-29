"""
Stage-specific models for the KL3M data client.
"""

from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class IndexMetadata:
    """Metadata section from an index."""

    dataset_id: str
    key_prefix: Optional[str]
    count: int
    created_at: datetime

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IndexMetadata":
        """Create an IndexMetadata instance from a dictionary."""
        created_at = data.get("created_at", datetime.now().isoformat())
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)

        return cls(
            dataset_id=data.get("dataset_id", ""),
            key_prefix=data.get("key_prefix"),
            count=data.get("count", 0),
            created_at=created_at,
        )


@dataclass
class DatasetIndex:
    """Index for a dataset."""

    objects: List[str]
    metadata: IndexMetadata

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DatasetIndex":
        """Create a DatasetIndex instance from a dictionary."""
        return cls(
            objects=data.get("objects", []),
            metadata=IndexMetadata.from_dict(data.get("metadata", {})),
        )

    def get_document_ids(self) -> Set[str]:
        """Extract document IDs from the object keys."""
        result = set()
        for key in self.objects:
            parts = key.split("/")
            if len(parts) >= 3:
                doc_id = parts[-1]
                if doc_id.endswith(".json"):
                    doc_id = doc_id[:-5]
                result.add(doc_id)
        return result
