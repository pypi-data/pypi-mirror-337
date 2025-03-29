#!/usr/bin/env python
"""
Simple usage example for the KL3M Data Client.

This script demonstrates how to retrieve and print the first 5 documents
from the USC dataset using streaming to efficiently process only what's needed.
"""

from kl3m_data_client import KL3MClient
from kl3m_data_client.models.common import Stage

# Initialize the client
client = KL3MClient(
    # These parameters are optional and will use environment variables if not provided
    # region="us-east-1",
    # aws_access_key_id="YOUR_ACCESS_KEY",
    # aws_secret_access_key="YOUR_SECRET_KEY",
    verbose=True,  # Enable verbose logging
)

# The dataset we want to retrieve documents from
DATASET_ID = "fdlp"

print(f"Streaming documents from dataset '{DATASET_ID}'...")

# Use the iterator to get document IDs efficiently - only request 5 documents
document_iterator = client.iter_documents(DATASET_ID, Stage.DOCUMENTS, limit=5)

# Process each document as it's streamed
doc_count = 0
for doc_id in document_iterator:
    doc_count += 1
    print(f"\nDocument {doc_count}: {doc_id}")

    # Retrieve the document
    document = client.get_document(DATASET_ID, doc_id, Stage.DOCUMENTS)

    if document:
        # Get the document content
        content = document.get_content(Stage.DOCUMENTS)

        if content:
            # Print document metadata
            print(f"  Source: {content.metadata.source}")
            print(f"  Title: {content.metadata.title or 'N/A'}")
            print(f"  Format: {content.metadata.format or 'N/A'}")

            # Print a short preview of the content
            content_preview = (
                content.content[:300] + "..."
                if len(content.content) > 300
                else content.content
            )
            print("\n  Original Document Preview:")
            print("  " + content_preview.replace("\n", "\n  "))

            print("\n" + "-" * 80)
        else:
            print("  Error: Could not retrieve document content")

        # Try to get data using the improved RepresentationList interface first
        representation_list = document.get_representation()

        if representation_list:
            # Print information in a more organized format
            print("\n  Representation Information:")
            print(f"  Document ID: {representation_list.document_id}")
            print(f"  Source: {representation_list.source}")

            # Get available MIME types
            mime_types = representation_list.get_available_mime_types()
            print(f"  Available representations: {', '.join(mime_types)}")

            # Get content for first available MIME type
            if mime_types:
                mime_type = mime_types[0]
                content = representation_list.get_content(mime_type)
                if content:
                    preview = content[:200] + "..." if len(content) > 200 else content
                    print(f"\n  {mime_type} Content Preview:")
                    print("  " + preview.replace("\n", "\n  "))

                # Show available tokenizers and token counts
                tokenizers = representation_list.get_available_tokenizers(mime_type)
                if tokenizers:
                    print(f"\n  Tokenizers: {', '.join(tokenizers)}")
                    print(
                        f"  Token count: {representation_list.token_count(mime_type, tokenizers[0])}"
                    )

            print("\n" + "-" * 80)
        else:
            # Fallback to the old method for backward compatibility
            representations = document.get_content(Stage.REPRESENTATIONS)

            if representations:
                # Print representation using its improved string representation
                print(f"\n  {representations}")
                print("\n" + "-" * 80)
            else:
                print("  Error: Could not retrieve representation content")

        # Now try to get the parquet stage data using the convenience method
        parquet_content = document.get_parquet()

        if parquet_content:
            # Print parquet information
            print("\n  Parquet Information:")
            print(f"  {parquet_content}")

            # We can provide more useful information about parquet data
            print(f"  Size: {parquet_content.size:,} bytes")
            print(f"  Document ID: {parquet_content.document_id}")

            # Use PyArrow enhancements to show more information
            table = parquet_content.get_table()
            if table:
                print(f"  Table Columns: {parquet_content.get_columns()}")
                print(f"  Number of rows: {len(table)}")

                # Show representation information
                print("\n  Representations:")
                representations = parquet_content.get_representations()
                for rep_type, tokens in representations.items():
                    print(f"    - {rep_type}: {len(tokens)} tokens")
            else:
                print("\n  Unable to parse parquet data as PyArrow table.")

            print(
                "\n  Note: Use parquet_content.save_to_file(filename) to save data to a file"
            )

            print("\n" + "-" * 80)
        else:
            print("  No parquet data available for this document")

    else:
        print("  Error: Document not found")

    # Stop after 5 documents (the limit should handle this, but just to be sure)
    if doc_count >= 5:
        break

print(f"\nProcessed {doc_count} documents from {DATASET_ID}.")
print("Done.")
