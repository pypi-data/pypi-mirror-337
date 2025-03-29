"""
Parquet utilities for the KL3M data client.
"""

import zlib
import html
import base64
import logging
from typing import Dict, List, Any, Optional

import pyarrow
import pyarrow.parquet
from tokenizers import Tokenizer

logger = logging.getLogger("kl3m_data_client")

# Define default tokenizer
DEFAULT_TOKENIZER_NAME = "alea-institute/kl3m-004-128k-cased"

# Default token type
DEFAULT_TOKEN_TYPE = pyarrow.uint32()

# Use a cache pattern instead of global variable
_tokenizer_cache = {}


def get_default_tokenizer() -> Tokenizer:
    """
    Get the default tokenizer, loading it only when needed.

    Returns:
        Tokenizer: The default tokenizer.
    """
    if DEFAULT_TOKENIZER_NAME not in _tokenizer_cache:
        _tokenizer_cache[DEFAULT_TOKENIZER_NAME] = Tokenizer.from_pretrained(
            DEFAULT_TOKENIZER_NAME
        )
    return _tokenizer_cache[DEFAULT_TOKENIZER_NAME]


def get_document_schema() -> pyarrow.Schema:
    """
    Get the schema for the document table.

    Returns:
        pyarrow.Schema: The schema for the document table.
    """
    schema = pyarrow.schema(
        [
            # source
            pyarrow.field("identifier", pyarrow.string()),
            pyarrow.field(
                "representations",
                pyarrow.map_(pyarrow.string(), pyarrow.list_(DEFAULT_TOKEN_TYPE)),
            ),
        ]
    )
    return schema


def serialize_document(document: Dict[str, Any], schema=None) -> Optional[bytes]:
    """
    Serialize a document to a pyarrow.Table.

    Args:
        document (Dict[str, Any]): The document to serialize.
        schema (pyarrow.Schema, optional): The schema for the document table.

    Returns:
        Optional[bytes]: The serialized document as parquet bytes, or None if serialization fails.
    """
    if schema is None:
        schema = get_document_schema()

    # get content token map
    token_map = []
    for content_type, record in document.get("representations", {}).items():
        try:
            # decode content
            if isinstance(record.get("content"), str):
                content = zlib.decompress(
                    base64.b64decode(record.get("content"))
                ).decode("utf-8")
            else:
                content = record.get("content", "")

            # if the content type is text/markdown or text/plain, unescape html
            # to get the actual content
            if content_type in ["text/markdown", "text/plain"]:
                if "&nbsp;" in content or "&#160;" in content:
                    try:
                        content = html.unescape(content)
                    except Exception as e:
                        logger.warning("Error while unescaping HTML: %s", e)
                        continue

            # encode content
            token_map.append(
                (content_type, get_default_tokenizer().encode(content).ids)
            )
        except Exception as e:
            logger.warning("Error while encoding content: %s", e)

    # create the table
    if len(token_map) < 1:
        return None

    table = pyarrow.table(
        {
            "identifier": [document.get("identifier", "")],
            "representations": [token_map],  # Wrap token_map in a list
        },
        schema=schema,
    )

    # write parquet bytes to buffer
    output_stream = pyarrow.BufferOutputStream()
    pyarrow.parquet.write_table(
        table, output_stream, write_statistics=False, store_schema=False
    )

    # return buffer as bytes
    return zlib.compress(output_stream.getvalue().to_pybytes())


def deserialize_document_bytes(document_bytes: bytes) -> Dict[str, Any]:
    """
    Deserialize a document from parquet bytes.

    This function tries multiple approaches to handle different parquet formats:
    1. First attempts to decompress and read with the standard schema
    2. If that fails, tries to read the raw bytes (no decompression)
    3. If that fails, tries to load without a predefined schema
    4. If all parsing attempts fail, returns an error document

    Args:
        document_bytes (bytes): The document bytes to deserialize.

    Returns:
        Dict[str, Any]: The deserialized document.
    """
    # Try multiple approaches in sequence
    table = None
    errors = []

    # Approach 1: Try decompressed with schema
    try:
        decompressed = zlib.decompress(document_bytes)
        table = pyarrow.parquet.read_table(
            pyarrow.BufferReader(decompressed),
            schema=get_document_schema(),
        )
    except Exception as e:
        errors.append(f"Standard schema approach: {str(e)}")

    # Approach 2: Try raw bytes with schema
    if table is None:
        try:
            table = pyarrow.parquet.read_table(
                pyarrow.BufferReader(document_bytes),
                schema=get_document_schema(),
            )
        except Exception as e:
            errors.append(f"Raw bytes approach: {str(e)}")

    # Approach 3: Try without schema
    if table is None:
        try:
            # Try decompressed without schema
            try:
                decompressed = zlib.decompress(document_bytes)
                table = pyarrow.parquet.read_table(pyarrow.BufferReader(decompressed))
            except:
                # Try raw bytes without schema
                table = pyarrow.parquet.read_table(pyarrow.BufferReader(document_bytes))
        except Exception as e:
            errors.append(f"No schema approach: {str(e)}")

    # If we successfully loaded a table, convert to dictionary
    if table is not None:
        try:
            # Get the document as a dictionary, handling different table formats
            doc = {}

            # Extract identifier/document_id
            if "identifier" in table.column_names:
                doc["identifier"] = table["identifier"][0].as_py()
            elif "document_id" in table.column_names:
                doc["identifier"] = table["document_id"][0].as_py()
            else:
                doc["identifier"] = ""

            # Extract representations
            if "representations" in table.column_names:
                try:
                    doc["representations"] = dict(table["representations"][0].as_py())
                except:
                    # Fallback for different representation formats
                    doc["representations"] = {}
            else:
                # For tables without explicit representations, create one from content and tokens
                doc["representations"] = {}

                # If there's content and tokens, add a text/plain representation
                if "content" in table.column_names and "tokens" in table.column_names:
                    doc["representations"]["text/plain"] = {
                        "content": table["content"][0].as_py(),
                        "tokens": {"default": table["tokens"][0].as_py()},
                    }

            return doc
        except Exception as e:
            errors.append(f"Table conversion: {str(e)}")

    # If all attempts failed, return an error document
    logger.warning(f"Error deserializing parquet: {'; '.join(errors)}")
    return {
        "identifier": "",
        "representations": {},
        "error": "Failed to parse parquet data: " + "; ".join(errors),
    }


def get_parquet_table(document_bytes: bytes) -> Optional[pyarrow.Table]:
    """
    Get a PyArrow Table from parquet bytes.

    Args:
        document_bytes (bytes): The document bytes to deserialize.

    Returns:
        Optional[pyarrow.Table]: The deserialized table, or None if deserialization fails.
    """
    try:
        # Decompress if compressed
        try:
            decompressed_bytes = zlib.decompress(document_bytes)
        except zlib.error:
            # If not compressed or invalid compression, use original bytes
            decompressed_bytes = document_bytes

        # Read table from bytes
        return pyarrow.parquet.read_table(pyarrow.BufferReader(decompressed_bytes))
    except Exception as e:
        logger.warning("Error reading parquet table: %s", e)
        return None


def get_table_schema(table: pyarrow.Table) -> pyarrow.Schema:
    """
    Get the schema of a PyArrow Table.

    Args:
        table (pyarrow.Table): The table to get the schema from.

    Returns:
        pyarrow.Schema: The schema of the table.
    """
    return table.schema


def get_table_columns(table: pyarrow.Table) -> List[str]:
    """
    Get the column names of a PyArrow Table.

    Args:
        table (pyarrow.Table): The table to get the column names from.

    Returns:
        List[str]: The column names of the table.
    """
    return table.column_names


def get_column_data(table: pyarrow.Table, column_name: str) -> Optional[List[Any]]:
    """
    Get data from a specific column in a PyArrow Table.

    Args:
        table (pyarrow.Table): The table to get data from.
        column_name (str): The name of the column to get data from.

    Returns:
        Optional[List[Any]]: The data from the column, or None if the column doesn't exist.
    """
    if column_name not in table.column_names:
        return None

    # Convert to Python objects
    return table[column_name].to_pylist()


def get_table_rows(table: pyarrow.Table) -> List[Dict[str, Any]]:
    """
    Convert a PyArrow Table to a list of dictionaries.

    Args:
        table (pyarrow.Table): The table to convert.

    Returns:
        List[Dict[str, Any]]: The table as a list of dictionaries.
    """
    rows = []
    for i in range(len(table)):
        row = {}
        for col in table.column_names:
            row[col] = table[col][i].as_py()
        rows.append(row)
    return rows


def create_simple_parquet(document_id: str, text: str) -> bytes:
    """
    Create a simple parquet file for testing.

    This is a simplified version that doesn't require a tokenizer, making it
    suitable for examples and tests.

    Args:
        document_id (str): The document ID.
        text (str): The text content.

    Returns:
        bytes: The parquet data.
    """
    # Create a simple schema with document_id and content
    schema = pyarrow.schema(
        [
            pyarrow.field("document_id", pyarrow.string()),
            pyarrow.field("content", pyarrow.string()),
            # Add a simple tokens field as a list of integers
            # This simulates the tokens field in real parquet files
            pyarrow.field("tokens", pyarrow.list_(pyarrow.int32())),
        ]
    )

    # Create a simple table with one row
    table = pyarrow.table(
        {
            "document_id": [document_id],
            "content": [text],
            # Simulate tokens by converting character codes to integers
            "tokens": [[ord(c) for c in text]],
        },
        schema=schema,
    )

    # Write the table to a buffer
    output_stream = pyarrow.BufferOutputStream()
    pyarrow.parquet.write_table(table, output_stream)

    # Return the buffer as bytes
    return output_stream.getvalue().to_pybytes()


def create_parquet_with_tokens(
    document_id: str, token_map: Dict[str, List[int]]
) -> bytes:
    """
    Create a parquet file with token representations for testing.

    This function creates a parquet file that matches the format used in the README examples,
    with an identifier field and a representations map field.

    Args:
        document_id (str): The document ID.
        token_map (Dict[str, List[int]]): Map of MIME types to token lists.

    Returns:
        bytes: The parquet data.
    """
    # Create a schema that matches the one used in the README
    schema = get_document_schema()

    # Format the token map as a list of tuples for PyArrow's map type
    token_map_list = [(mime_type, tokens) for mime_type, tokens in token_map.items()]

    # Create a table with one row
    table = pyarrow.table(
        {
            "identifier": [document_id],
            "representations": [token_map_list],
        },
        schema=schema,
    )

    # Write the table to a buffer
    output_stream = pyarrow.BufferOutputStream()
    pyarrow.parquet.write_table(table, output_stream)

    # Return the buffer as bytes
    return output_stream.getvalue().to_pybytes()
