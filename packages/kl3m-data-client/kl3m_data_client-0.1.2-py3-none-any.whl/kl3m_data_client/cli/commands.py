"""
Command-line interface for the KL3M data client.
"""

import sys
import os
import argparse
import logging

from rich.console import Console

from kl3m_data_client import KL3MClient
from kl3m_data_client.models.common import Stage
from kl3m_data_client.utils.console import (
    configure_logging,
    create_dataset_status_table,
    create_dataset_list_table,
)


# Set up console
console = Console()
logger = logging.getLogger("kl3m_data_client")


def list_command(args: argparse.Namespace) -> int:
    """
    List all available datasets.

    Args:
        args: Command-line arguments.

    Returns:
        Exit code.
    """
    # Initialize client
    client = KL3MClient(
        region=args.region,
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        verbose=args.verbose,
    )

    # Get datasets
    datasets = client.list_datasets()

    # Display as a table
    table = create_dataset_list_table(datasets)
    console.print(table)

    return 0


def status_command(args: argparse.Namespace) -> int:
    """
    Show the status of a dataset.

    Args:
        args: Command-line arguments.

    Returns:
        Exit code.
    """
    # Initialize client
    client = KL3MClient(
        region=args.region,
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        verbose=args.verbose,
    )

    # Get dataset status
    status = client.get_dataset_status(args.dataset_id, args.key_prefix)

    # Display as a table
    table = create_dataset_status_table(status)
    console.print(table)

    # Save to CSV if requested
    if args.csv:
        import csv

        try:
            with open(args.csv, "w", newline="", encoding="utf-8") as csvfile:
                csvwriter = csv.writer(csvfile)
                # Write header
                csvwriter.writerow(
                    [
                        "Dataset",
                        "Documents",
                        "Representations",
                        "Parquet",
                        "Missing Rep.",
                        "Missing Parq.",
                        "Is Complete",
                    ]
                )
                # Write data
                csvwriter.writerow(
                    [
                        status.dataset_id,
                        status.document_count,
                        status.representation_count,
                        status.parquet_count,
                        status.missing_representations,
                        status.missing_parquet,
                        status.is_complete,
                    ]
                )
            console.print(f"[green]CSV output written to {args.csv}[/green]")
        except Exception as e:
            console.print(f"[red]Error writing CSV: {e}[/red]")
            return 1

    return 0


def list_documents_command(args: argparse.Namespace) -> int:
    """
    List all documents in a dataset.

    Args:
        args: Command-line arguments.

    Returns:
        Exit code.
    """
    # Initialize client
    client = KL3MClient(
        region=args.region,
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        verbose=args.verbose,
    )

    # Convert stage string to enum
    try:
        stage = Stage[args.stage.upper()]
    except KeyError:
        console.print(f"[red]Invalid stage: {args.stage}[/red]")
        return 1

    # If we only need the count or a limited number of documents,
    # use the streaming approach to avoid loading all documents
    if args.count or args.limit:
        if args.count:
            # Just count the documents
            count = 0
            for _ in client.iter_documents(args.dataset_id, stage, args.key_prefix):
                count += 1
                if args.limit and count >= args.limit:
                    break

            console.print(
                f"Found {count} documents in {args.dataset_id} ({stage.value})"
            )

            # Write count to output file if requested
            if args.output:
                try:
                    with open(args.output, "w", encoding="utf-8") as f:
                        f.write(f"{count}\n")
                    console.print(f"[green]Count written to {args.output}[/green]")
                except Exception as e:
                    console.print(f"[red]Error writing to file: {e}[/red]")
                    return 1
        else:
            # Get limited documents
            document_ids = list(
                client.iter_documents(
                    args.dataset_id, stage, args.key_prefix, limit=args.limit
                )
            )

            # Display document IDs
            if document_ids:
                for doc_id in document_ids:
                    console.print(doc_id)
                console.print(f"\nTotal: {len(document_ids)} documents")
            else:
                console.print(
                    f"No documents found in {args.dataset_id} ({stage.value})"
                )

            # Write to file if requested
            if args.output:
                try:
                    with open(args.output, "w", encoding="utf-8") as f:
                        for doc_id in document_ids:
                            f.write(f"{doc_id}\n")
                    console.print(
                        f"[green]Document IDs written to {args.output}[/green]"
                    )
                except Exception as e:
                    console.print(f"[red]Error writing to file: {e}[/red]")
                    return 1
    else:
        # Get all documents (legacy behavior)
        document_ids = client.list_documents(args.dataset_id, stage, args.key_prefix)

        # Display results
        if document_ids:
            for doc_id in document_ids:
                console.print(doc_id)
            console.print(f"\nTotal: {len(document_ids)} documents")
        else:
            console.print(f"No documents found in {args.dataset_id} ({stage.value})")

        # Write to file if requested
        if args.output:
            try:
                with open(args.output, "w", encoding="utf-8") as f:
                    for doc_id in document_ids:
                        f.write(f"{doc_id}\n")
                console.print(f"[green]Document IDs written to {args.output}[/green]")
            except Exception as e:
                console.print(f"[red]Error writing to file: {e}[/red]")
                return 1

    return 0


def export_jsonl_command(args: argparse.Namespace) -> int:
    """
    Export dataset to JSONL file.

    Args:
        args: Command-line arguments.

    Returns:
        Exit code.
    """
    # Initialize client
    client = KL3MClient(
        region=args.region,
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        verbose=args.verbose,
    )

    # Convert stage string to enum
    try:
        source_stage = Stage[args.source_stage.upper()]
    except KeyError:
        console.print(f"[red]Invalid stage: {args.source_stage}[/red]")
        return 1

    # Export to JSONL
    try:
        count = client.export_to_jsonl(
            args.dataset_id,
            args.output_path,
            args.key_prefix,
            source_stage,
            args.max_documents,
            args.tokenizer,
            args.representation,
            not args.no_deduplicate,
            args.include_metrics,
        )

        console.print(
            f"[green]Successfully exported {count} documents to {args.output_path}[/green]"
        )
        return 0
    except Exception as e:
        console.print(f"[red]Error exporting dataset: {e}[/red]")
        return 1


def inspect_document_command(args: argparse.Namespace) -> int:
    """
    Inspect a document in a dataset.

    Args:
        args: Command-line arguments.

    Returns:
        Exit code.
    """
    # Initialize client
    client = KL3MClient(
        region=args.region,
        aws_access_key_id=args.aws_access_key_id,
        aws_secret_access_key=args.aws_secret_access_key,
        verbose=args.verbose,
    )

    # Convert stage string to enum
    try:
        stage = Stage[args.stage.upper()]
    except KeyError:
        console.print(f"[red]Invalid stage: {args.stage}[/red]")
        return 1

    # Get document
    document = client.get_document(args.dataset_id, args.document_id, stage)
    if not document:
        console.print(
            f"[red]Document {args.document_id} not found in {args.dataset_id} ({stage.value})[/red]"
        )
        return 1

    # Get document content based on stage
    document_content = None
    representation_content = None
    parquet_content = None
    content_type = ""

    if stage == Stage.DOCUMENTS:
        document_content = document.get_document_content()
        if not document_content:
            console.print(
                f"[red]Unable to retrieve document content for {args.document_id}[/red]"
            )
            return 1
        content_type = "document"
    elif stage == Stage.REPRESENTATIONS:
        representation_content = document.get_representation_content()
        if not representation_content:
            console.print(
                f"[red]Unable to retrieve representation content for {args.document_id}[/red]"
            )
            return 1
        content_type = "representation"
    elif stage == Stage.PARQUET:
        parquet_content = document.get_parquet()
        if not parquet_content:
            console.print(
                f"[red]Unable to retrieve parquet content for {args.document_id}[/red]"
            )
            return 1
        content_type = "parquet"
    else:
        console.print(f"[red]Invalid stage: {stage.value}[/red]")
        return 1

    # Write to file if requested
    if args.output:
        import json

        try:
            # Handle each content type separately
            if content_type == "document" and document_content:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(
                        document_content.__dict__,
                        f,
                        default=lambda o: o.__dict__,
                        indent=2,
                    )
            elif content_type == "representation" and representation_content:
                with open(args.output, "w", encoding="utf-8") as f:
                    json.dump(
                        representation_content.__dict__,
                        f,
                        default=lambda o: o.__dict__,
                        indent=2,
                    )
            elif content_type == "parquet" and parquet_content:
                with open(args.output, "wb") as f:
                    # Ensure we're writing bytes for ParquetContent
                    if hasattr(parquet_content, "to_bytes"):
                        f.write(parquet_content.to_bytes())
                    elif isinstance(parquet_content, bytes):
                        f.write(parquet_content)
                    else:
                        # Fallback - convert to JSON and encode
                        f.write(
                            json.dumps(
                                parquet_content.__dict__, default=lambda o: o.__dict__
                            ).encode("utf-8")
                        )

            console.print(f"[green]Document content written to {args.output}[/green]")
        except Exception as e:
            console.print(f"[red]Error writing to file: {e}[/red]")
            return 1
    else:
        # Display document content summary based on stage type
        if content_type == "document" and document_content:
            # We already have the document_content
            console.print(
                f"[bold]Document ID:[/bold] {document_content.metadata.identifier}"
            )
            console.print(f"[bold]Source:[/bold] {document_content.metadata.source}")
            console.print(
                f"[bold]Title:[/bold] {document_content.metadata.title or 'N/A'}"
            )
            console.print(
                f"[bold]Format:[/bold] {document_content.metadata.format or 'N/A'}"
            )

            # Show content preview
            if hasattr(document_content, "content") and document_content.content:
                text = document_content.content
                preview = text[:500] + ("..." if len(text) > 500 else "")
                console.print("\n[bold]Content Preview:[/bold]")
                console.print(preview)

        elif content_type == "representation" and representation_content:
            # We already have the representation_content
            # Get the first document
            doc_data = representation_content.get_document_data(0)
            if doc_data:
                console.print(
                    f"[bold]Document ID:[/bold] {doc_data.get('identifier', 'N/A')}"
                )
                console.print(f"[bold]Source:[/bold] {doc_data.get('source', 'N/A')}")

                # Show representations
                if "representations" in doc_data:
                    console.print("\n[bold]Available Representations:[/bold]")
                    for rep_type in doc_data["representations"]:
                        console.print(f"- {rep_type}")

                # Show text preview for specified representation
                if args.representation:
                    text_content = representation_content.get_text_content(
                        args.representation
                    )
                    if text_content:
                        preview = text_content[:500] + (
                            "..." if len(text_content) > 500 else ""
                        )
                        console.print(
                            f"\n[bold]Content Preview ({args.representation}):[/bold]"
                        )
                        console.print(preview)

        elif content_type == "parquet" and parquet_content:
            # Display parquet information
            console.print(f"[bold]Parquet Content:[/bold] {parquet_content}")
            console.print(f"[bold]Size:[/bold] {parquet_content.size:,} bytes")
            console.print(f"[bold]Document ID:[/bold] {parquet_content.document_id}")

            # Show PyArrow table information if available
            table = parquet_content.get_table()
            if table:
                console.print(
                    f"[bold]Table Columns:[/bold] {parquet_content.get_columns()}"
                )
                console.print(f"[bold]Number of rows:[/bold] {len(table)}")

                # Show representation information
                console.print("\n[bold]Representations:[/bold]")
                representations = parquet_content.get_representations()
                for rep_type, tokens in representations.items():
                    console.print(f"  - {rep_type}: {len(tokens)} tokens")

    console.print(
        "[yellow]Note: Use --output to save binary parquet data to a file[/yellow]"
    )

    return 0


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments.
    """
    parser = argparse.ArgumentParser(
        description="KL3M Data Client",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    # Global options
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Enable verbose logging"
    )
    parser.add_argument(
        "--region", help="AWS region", default=os.environ.get("AWS_REGION", "us-east-1")
    )
    parser.add_argument(
        "--aws-access-key-id",
        help="AWS access key ID",
        default=os.environ.get("AWS_ACCESS_KEY_ID"),
    )
    parser.add_argument(
        "--aws-secret-access-key",
        help="AWS secret access key",
        default=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", required=True)

    # List datasets command
    list_parser = subparsers.add_parser("list", help="List all datasets")
    list_parser.set_defaults(func=list_command)

    # Status command
    status_parser = subparsers.add_parser("status", help="Show dataset status")
    status_parser.add_argument("dataset_id", help="Dataset ID")
    status_parser.add_argument("--key-prefix", help="Key prefix to filter objects")
    status_parser.add_argument("--csv", help="Path to save results as CSV file")
    status_parser.set_defaults(func=status_command)

    # List documents command
    documents_parser = subparsers.add_parser(
        "documents", help="List documents in a dataset"
    )
    documents_parser.add_argument("dataset_id", help="Dataset ID")
    documents_parser.add_argument(
        "--stage",
        choices=["documents", "representations", "parquet"],
        default="documents",
        help="Stage to list documents from",
    )
    documents_parser.add_argument("--key-prefix", help="Key prefix to filter objects")
    documents_parser.add_argument(
        "--output", help="Path to save document IDs to a file"
    )
    documents_parser.add_argument(
        "--count", action="store_true", help="Show only the count of documents"
    )
    documents_parser.add_argument(
        "--limit", type=int, help="Limit the number of documents to retrieve"
    )
    documents_parser.set_defaults(func=list_documents_command)

    # Export JSONL command
    export_parser = subparsers.add_parser(
        "export-jsonl", help="Export dataset to JSONL file"
    )
    export_parser.add_argument("dataset_id", help="Dataset ID")
    export_parser.add_argument("output_path", help="Path to output JSONL file")
    export_parser.add_argument(
        "--source-stage",
        choices=["representations", "parquet"],
        default="parquet",
        help="Source stage to export from",
    )
    export_parser.add_argument("--key-prefix", help="Key prefix to filter objects")
    export_parser.add_argument(
        "--max-documents", type=int, help="Maximum number of documents to export"
    )
    export_parser.add_argument(
        "--tokenizer", default="cl100k_base", help="Tokenizer name"
    )
    export_parser.add_argument(
        "--representation", default="text/plain", help="Representation MIME type"
    )
    export_parser.add_argument(
        "--no-deduplicate", action="store_true", help="Disable deduplication"
    )
    export_parser.add_argument(
        "--include-metrics",
        action="store_true",
        help="Include detailed metrics in output",
    )
    export_parser.set_defaults(func=export_jsonl_command)

    # Inspect document command
    inspect_parser = subparsers.add_parser("inspect", help="Inspect a document")
    inspect_parser.add_argument("dataset_id", help="Dataset ID")
    inspect_parser.add_argument("document_id", help="Document ID")
    inspect_parser.add_argument(
        "--stage",
        choices=["documents", "representations", "parquet"],
        default="documents",
        help="Stage to inspect document from",
    )
    inspect_parser.add_argument(
        "--output", help="Path to save document content to a file"
    )
    inspect_parser.add_argument(
        "--representation",
        default="text/plain",
        help="Representation MIME type to display",
    )
    inspect_parser.set_defaults(func=inspect_document_command)

    return parser.parse_args()


def main() -> int:
    """
    Main entry point for the CLI.

    Returns:
        Exit code.
    """
    try:
        args = parse_args()

        # Configure logging
        configure_logging(args.verbose, console)

        # Run the appropriate command
        return args.func(args)

    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")
        return 130

    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        if "--verbose" in sys.argv or "-v" in sys.argv:
            console.print_exception(show_locals=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
