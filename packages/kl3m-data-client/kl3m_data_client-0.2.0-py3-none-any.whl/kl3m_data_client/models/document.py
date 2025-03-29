"""
Document data models for the KL3M data client.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass


@dataclass
class DocumentMetadata:
    """Metadata for a document."""

    identifier: str
    source: str
    title: Optional[str] = None
    date: Optional[str] = None
    format: Optional[str] = None
    language: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DocumentMetadata":
        """Create a DocumentMetadata instance from a dictionary."""
        return cls(
            identifier=data.get("identifier", ""),
            source=data.get("source", ""),
            title=data.get("title"),
            date=data.get("date"),
            format=data.get("format"),
            language=data.get("language"),
        )


@dataclass
class DocumentContent:
    """Content of a document from the Documents stage."""

    content: str
    metadata: DocumentMetadata

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DocumentContent":
        """Create a DocumentContent instance from a dictionary."""
        return cls(
            content=data.get("content", ""),
            metadata=DocumentMetadata.from_dict(data),
        )


@dataclass
class SingleRepresentation:
    """A single representation of a document (e.g., text/plain, text/markdown)."""

    mime_type: str
    content: Optional[str]
    tokens: Dict[str, List[int]]

    @classmethod
    def from_dict(cls, mime_type: str, data: Dict[str, Any]) -> "SingleRepresentation":
        """Create a SingleRepresentation instance from a dictionary."""
        return cls(
            mime_type=mime_type,
            content=data.get("content"),
            tokens=data.get("tokens", {}),
        )

    def get_tokens(self, tokenizer: str = "cl100k_base") -> Optional[List[int]]:
        """Get tokens for a specific tokenizer."""
        return self.tokens.get(tokenizer)

    def get_available_tokenizers(self) -> List[str]:
        """Get a list of available tokenizers."""
        return list(self.tokens.keys())

    def token_count(self, tokenizer: str = "cl100k_base") -> int:
        """Get the token count for a specific tokenizer."""
        tokens = self.get_tokens(tokenizer)
        return len(tokens) if tokens else 0

    def __str__(self) -> str:
        """Return a readable string representation."""
        content_preview = ""
        if self.content:
            preview = self.content[:50].replace("\n", " ")
            content_preview = (
                f', content: "{preview}{"..." if len(self.content) > 50 else ""}"'
            )

        token_info = ", ".join(
            f"{tokenizer}: {len(tokens)} tokens"
            for tokenizer, tokens in self.tokens.items()
        )

        return f"<{self.mime_type}{content_preview}, tokens: {{{token_info if token_info else 'none'}}}>"


@dataclass
class RepresentationList:
    """A container for all representations of a document."""

    document_id: str
    source: str
    metadata: Dict[str, Any]
    representations: Dict[str, SingleRepresentation]
    success: bool = True
    error: Optional[str] = None

    @classmethod
    def from_document_data(cls, document_data: Dict[str, Any]) -> "RepresentationList":
        """Create a RepresentationList instance from document data dictionary."""
        # Extract representations
        rep_dict = {}
        for mime_type, rep_data in document_data.get("representations", {}).items():
            rep_dict[mime_type] = SingleRepresentation.from_dict(mime_type, rep_data)

        return cls(
            document_id=document_data.get("identifier", ""),
            source=document_data.get("source", ""),
            metadata=document_data.get("metadata", {}),
            representations=rep_dict,
            success=document_data.get("success", True),
            error=document_data.get("error"),
        )

    def __str__(self) -> str:
        """Return a readable string representation."""
        reps_str = ", ".join(str(rep) for rep in self.representations.values())
        metadata_str = ", ".join(f"{k}: {v}" for k, v in self.metadata.items() if v)

        parts = [f"Document: {self.document_id}"]
        parts.append(f"Source: {self.source}")

        if metadata_str:
            parts.append(f"Metadata: {{{metadata_str}}}")

        if self.representations:
            parts.append(f"Representations: [{reps_str}]")
        else:
            parts.append("Representations: []")

        if not self.success and self.error:
            parts.append(f"Error: {self.error}")

        return "\n".join(parts)

    def get_representation(
        self, mime_type: str = "text/plain"
    ) -> Optional[SingleRepresentation]:
        """Get a specific representation by MIME type."""
        return self.representations.get(mime_type)

    def get_content(self, mime_type: str = "text/plain") -> Optional[str]:
        """Get text content for a specific representation."""
        rep = self.get_representation(mime_type)
        return rep.content if rep else None

    def get_tokens(
        self, mime_type: str = "text/plain", tokenizer: str = "cl100k_base"
    ) -> Optional[List[int]]:
        """Get tokens for a specific representation and tokenizer."""
        rep = self.get_representation(mime_type)
        return rep.get_tokens(tokenizer) if rep else None

    def get_available_mime_types(self) -> List[str]:
        """Get a list of available MIME types."""
        return list(self.representations.keys())

    def get_available_tokenizers(self, mime_type: str = "text/plain") -> List[str]:
        """Get a list of available tokenizers for a specific representation."""
        rep = self.get_representation(mime_type)
        return rep.get_available_tokenizers() if rep else []

    def token_count(
        self, mime_type: str = "text/plain", tokenizer: str = "cl100k_base"
    ) -> int:
        """Get the token count for a specific representation and tokenizer."""
        rep = self.get_representation(mime_type)
        return rep.token_count(tokenizer) if rep else 0

    def summarize(self) -> Dict[str, Any]:
        """Get a summary of the representation."""
        return {
            "document_id": self.document_id,
            "source": self.source,
            "mime_types": self.get_available_mime_types(),
            "token_counts": {
                mime_type: {
                    tokenizer: self.token_count(mime_type, tokenizer)
                    for tokenizer in self.get_available_tokenizers(mime_type)
                }
                for mime_type in self.get_available_mime_types()
            },
        }


@dataclass
class ParquetContent:
    """Content of a document from the Parquet stage with PyArrow support."""

    document_id: str
    data: bytes
    size: int
    _table: Optional[Any] = None
    _document: Optional[Dict[str, Any]] = None

    @classmethod
    def from_bytes(cls, document_id: str, data: bytes) -> "ParquetContent":
        """Create a ParquetContent instance from bytes."""
        return cls(
            document_id=document_id,
            data=data,
            size=len(data),
        )

    def __str__(self) -> str:
        """Return a readable string representation."""
        # Include column info if table is loaded
        table_info = ""
        if self._table is not None:
            columns = self.get_columns()
            table_info = f", columns={columns}"

        return f"ParquetContent(document_id={self.document_id}, size={self.size} bytes{table_info})"

    def save_to_file(self, file_path: str) -> bool:
        """Save the parquet data to a file."""
        try:
            with open(file_path, "wb") as f:
                f.write(self.data)
            return True
        except Exception:
            return False

    def get_data(self) -> bytes:
        """Get the raw parquet data."""
        return self.data

    def get_table(self) -> Optional[Any]:
        """
        Get the PyArrow Table representation of the parquet data.

        Returns:
            Optional[pyarrow.Table]: The PyArrow Table, or None if loading fails.
        """
        if self._table is None:
            # Import here to avoid circular imports
            from kl3m_data_client.utils.parquet_utils import get_parquet_table

            self._table = get_parquet_table(self.data)
        return self._table

    def get_schema(self) -> Optional[Any]:
        """
        Get the schema of the parquet data.

        Returns:
            Optional[pyarrow.Schema]: The schema, or None if loading fails.
        """
        table = self.get_table()
        if table is None:
            return None

        # Import here to avoid circular imports
        from kl3m_data_client.utils.parquet_utils import get_table_schema

        return get_table_schema(table)

    def get_columns(self) -> List[str]:
        """
        Get the column names of the parquet data.

        Returns:
            List[str]: The column names, or an empty list if loading fails.
        """
        table = self.get_table()
        if table is None:
            return []

        # Import here to avoid circular imports
        from kl3m_data_client.utils.parquet_utils import get_table_columns

        return get_table_columns(table)

    def get_column_data(self, column_name: str) -> Optional[List[Any]]:
        """
        Get data from a specific column in the parquet data.

        Args:
            column_name (str): The name of the column to get data from.

        Returns:
            Optional[List[Any]]: The data from the column, or None if the column doesn't exist.
        """
        table = self.get_table()
        if table is None:
            return None

        # Import here to avoid circular imports
        from kl3m_data_client.utils.parquet_utils import get_column_data

        return get_column_data(table, column_name)

    def get_rows(self) -> List[Dict[str, Any]]:
        """
        Get all rows from the parquet data as dictionaries.

        Returns:
            List[Dict[str, Any]]: The rows as dictionaries, or an empty list if loading fails.
        """
        table = self.get_table()
        if table is None:
            return []

        # Import here to avoid circular imports
        from kl3m_data_client.utils.parquet_utils import get_table_rows

        return get_table_rows(table)

    def get_document(self) -> Dict[str, Any]:
        """
        Get the document from the parquet data.

        Returns:
            Dict[str, Any]: The document, or an empty dictionary if loading fails.
        """
        if self._document is None:
            # Check if we already have a table loaded
            table = self.get_table()

            if table is not None and "document_id" in table.column_names:
                # Simple case: extract from table
                rows = []
                from kl3m_data_client.utils.parquet_utils import get_table_rows

                rows = get_table_rows(table)

                if rows:
                    self._document = rows[0]
                    # Ensure it has the identifier field
                    if (
                        "document_id" in self._document
                        and "identifier" not in self._document
                    ):
                        self._document["identifier"] = self._document["document_id"]
                else:
                    self._document = {
                        "identifier": self.document_id,
                        "error": "No rows in table",
                    }
            else:
                # Try the complex case for real KL3M parquet data
                from kl3m_data_client.utils.parquet_utils import (
                    deserialize_document_bytes,
                )

                try:
                    self._document = deserialize_document_bytes(self.data)
                except Exception as e:
                    self._document = {"identifier": self.document_id, "error": str(e)}

        return self._document

    def get_representations(self) -> Dict[str, List[int]]:
        """
        Get the representation tokens from the parquet data.

        Returns:
            Dict[str, List[int]]: A dictionary mapping representation types to token lists.
        """
        document = self.get_document()

        # Check for standard KL3M format with "representations" field
        if "representations" in document:
            return document.get("representations", {})

        # Check for simplified format with "tokens" field
        if "tokens" in document:
            # For simple format, create a default representation with the tokens
            return {"text/plain": document.get("tokens", [])}

        # No tokens found
        return {}


@dataclass
class RepresentationContent:
    """Content of a document from the Representations stage."""

    documents: List[Dict[str, Any]]

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RepresentationContent":
        """Create a RepresentationContent instance from a dictionary."""
        return cls(
            documents=data.get("documents", []),
        )

    def __str__(self) -> str:
        """Return a more readable string representation."""
        doc_count = len(self.documents)

        if doc_count == 0:
            return "RepresentationContent(empty)"

        # If there's only one document, convert it to a RepresentationList and use its string representation
        if doc_count == 1:
            rep_list = self.get_representation(0)
            if rep_list:
                return f"RepresentationContent:\n{str(rep_list)}"

        # For multiple documents, just show a summary
        return f"RepresentationContent({doc_count} documents)"

    def get_document_data(self, index: int = 0) -> Optional[Dict[str, Any]]:
        """Get a specific document from the representation content."""
        if not self.documents or index >= len(self.documents):
            return None
        return self.documents[index]

    def get_representation(self, index: int = 0) -> Optional[RepresentationList]:
        """Get a specific document as a RepresentationList object."""
        doc_data = self.get_document_data(index)
        if not doc_data:
            return None
        return RepresentationList.from_document_data(doc_data)

    def get_text_content(
        self, mime_type: str = "text/plain", index: int = 0
    ) -> Optional[str]:
        """Get the text content of a specific representation."""
        doc = self.get_document_data(index)
        if not doc:
            return None

        representations = doc.get("representations", {})
        rep = representations.get(mime_type, {})
        return rep.get("content")

    def get_tokens(
        self,
        tokenizer: str = "cl100k_base",
        mime_type: str = "text/plain",
        index: int = 0,
    ) -> Optional[List[int]]:
        """Get the tokens of a specific representation."""
        doc = self.get_document_data(index)
        if not doc:
            return None

        representations = doc.get("representations", {})
        rep = representations.get(mime_type, {})
        tokens = rep.get("tokens", {})
        return tokens.get(tokenizer)

    def get_all_representations(self) -> List[RepresentationList]:
        """Get all documents as RepresentationList objects."""
        return [
            RepresentationList.from_document_data(doc) for doc in self.documents if doc
        ]
