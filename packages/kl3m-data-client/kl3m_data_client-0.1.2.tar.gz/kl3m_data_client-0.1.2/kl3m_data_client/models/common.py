"""
Common models and enums for the KL3M data client.
"""

from enum import Enum
from typing import Dict, Any
from dataclasses import dataclass


class Stage(Enum):
    """Enum representing the three stages of the KL3M pipeline."""

    DOCUMENTS = "documents"
    REPRESENTATIONS = "representations"
    PARQUET = "parquet"
    INDEX = "index"


@dataclass
class DatasetStatus:
    """Status of a dataset in the pipeline."""

    dataset_id: str
    document_count: int
    representation_count: int
    parquet_count: int
    missing_representations: int
    missing_parquet: int

    @property
    def is_complete(self) -> bool:
        """Check if the dataset processing is complete."""
        return self.missing_representations == 0 and self.missing_parquet == 0

    @property
    def total_documents(self) -> int:
        """Get the total number of documents."""
        return self.document_count

    def as_dict(self) -> Dict[str, Any]:
        """Convert the status to a dictionary."""
        return {
            "dataset_id": self.dataset_id,
            "document_count": self.document_count,
            "representation_count": self.representation_count,
            "parquet_count": self.parquet_count,
            "missing_representations": self.missing_representations,
            "missing_parquet": self.missing_parquet,
            "is_complete": self.is_complete,
        }


@dataclass
class ProcessingResult:
    """Result of a processing operation."""

    processed_count: int
    error_count: int
    duration_seconds: float

    @property
    def total_count(self) -> int:
        """Get the total number of documents processed."""
        return self.processed_count + self.error_count

    @property
    def success_rate(self) -> float:
        """Get the success rate as a percentage."""
        if self.total_count == 0:
            return 100.0
        return (self.processed_count / self.total_count) * 100

    @property
    def docs_per_second(self) -> float:
        """Get the processing rate in documents per second."""
        if self.duration_seconds <= 0:
            return 0.0
        return self.processed_count / self.duration_seconds
