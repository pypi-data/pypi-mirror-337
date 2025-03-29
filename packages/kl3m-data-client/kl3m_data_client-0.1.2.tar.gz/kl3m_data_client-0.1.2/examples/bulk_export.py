#!/usr/bin/env python
"""
Bulk Export Example for KL3M Data Client.

This script demonstrates how to export multiple datasets in parallel
with customizable filtering and processing options.
"""

import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Any, Optional, Callable

from kl3m_data_client import KL3MClient
from kl3m_data_client.models.common import Stage
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Bulk export KL3M datasets")
    parser.add_argument(
        "datasets", nargs="+", help="Dataset IDs to export (space-separated)"
    )
    parser.add_argument(
        "--output-dir", default="exports", help="Output directory for exported files"
    )
    parser.add_argument(
        "--max-documents",
        type=int,
        default=None,
        help="Maximum documents to export per dataset (default: all)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Limit export to first N documents per dataset (same as max-documents, provided for compatibility)",
    )
    parser.add_argument(
        "--stage",
        choices=["documents", "representations", "parquet"],
        default="parquet",
        help="Source stage for export (default: parquet)",
    )
    parser.add_argument(
        "--representation",
        default="text/plain",
        help="Representation MIME type to export (default: text/plain)",
    )
    parser.add_argument(
        "--workers", type=int, default=3, help="Number of parallel export workers"
    )
    parser.add_argument(
        "--compress", action="store_true", help="Compress output files with gzip"
    )
    parser.add_argument(
        "--exclude-content",
        action="store_true",
        help="Exclude document content from export",
    )
    parser.add_argument("--filter", help="Path to JSON file with filter criteria")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


def discover_representation_type(
    client: KL3MClient, dataset_id: str, progress: Optional[Progress] = None
) -> str:
    """
    Detect available representation types for a dataset by examining sample documents.

    Args:
        client: KL3M client
        dataset_id: Dataset ID to examine
        progress: Progress tracker for displaying messages

    Returns:
        Best available MIME type to use (defaults to text/plain if nothing found)
    """
    # Common representation types to check in order of preference
    representation_types = [
        "text/plain",
        "text/markdown",
        "text/html",
        "application/pdf",
    ]

    # Get a sample document
    try:
        # Get first document ID
        doc_id = next(client.iter_documents(dataset_id, Stage.REPRESENTATIONS, limit=1))

        # Get the document
        document = client.get_document(dataset_id, doc_id, Stage.REPRESENTATIONS)

        if document:
            # Get representation content
            rep_list = document.get_representation()

            if rep_list and rep_list.representations:
                # Get available MIME types
                available_types = rep_list.get_available_mime_types()

                # Find the first available type from our preference list
                for rep_type in representation_types:
                    if rep_type in available_types:
                        if progress:
                            progress.console.print(
                                f"[green]Found representation type: {rep_type}[/green]"
                            )
                        return rep_type

                # If none of our preferred types are available, use the first available
                rep_type = available_types[0]
                if progress:
                    progress.console.print(
                        f"[yellow]Using non-standard representation type: {rep_type}[/yellow]"
                    )
                return rep_type

    except Exception as e:
        if progress:
            progress.console.print(
                f"[yellow]Error discovering representation type: {e}[/yellow]"
            )

    # Default to text/plain
    if progress:
        progress.console.print(
            "[yellow]No representation types found, defaulting to text/plain[/yellow]"
        )
    return "text/plain"


def export_dataset(
    client: KL3MClient,
    dataset_id: str,
    output_dir: str,
    source_stage: Stage,
    max_documents: Optional[int] = None,
    compress: bool = False,
    exclude_content: bool = False,
    filter_func: Optional[Callable[[Dict[str, Any]], bool]] = None,
    progress: Optional[Progress] = None,
    task_id: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Export a single dataset with optional filtering.

    Args:
        client: KL3M client
        dataset_id: Dataset ID to export
        output_dir: Output directory
        source_stage: Source stage for export
        max_documents: Maximum documents to export
        compress: Compress output file
        exclude_content: Exclude document content
        filter_func: Optional filter function
        progress: Progress tracker
        task_id: Task ID for progress tracking

    Returns:
        Dictionary with export results
    """
    start_time = time.time()

    # Create output filename
    os.makedirs(output_dir, exist_ok=True)
    extension = ".jsonl.gz" if compress else ".jsonl"
    output_path = os.path.join(output_dir, f"{dataset_id}{extension}")

    # Initialize counters
    total_docs = 0
    exported_docs = 0
    filtered_docs = 0

    # Get stage enum from string
    stage_enum = getattr(Stage, source_stage.upper())

    # For parquet stage, use REPRESENTATIONS stage instead since the export functionality
    # in operations/export.py cannot properly handle parquet binary data
    if stage_enum == Stage.PARQUET and progress and task_id is not None:
        progress.console.print(
            f"[bold yellow]Warning: Switching from PARQUET to REPRESENTATIONS stage for {dataset_id} due to binary data handling limitations[/bold yellow]"
        )
        stage_enum = Stage.REPRESENTATIONS

    # Export with or without filtering
    if filter_func:
        # Manual export with filtering
        with open(output_path, "wt") as f:
            for doc in client.iter_jsonl_export(
                dataset_id=dataset_id,
                source_stage=stage_enum,
                max_documents=max_documents,
                deduplicate=True,
                exclude_content=exclude_content,
            ):
                total_docs += 1

                # Apply filter
                if filter_func(doc):
                    f.write(json.dumps(doc) + "\n")
                    exported_docs += 1
                else:
                    filtered_docs += 1

                # Update progress
                if progress and task_id is not None:
                    progress.update(task_id, completed=total_docs)
    else:
        # Use built-in export function
        # If compress is True, we should create a gzipped output path ourselves
        export_output_path = output_path

        # Create a custom iterator with content exclusion if needed
        if exclude_content:
            # Custom export with content exclusion
            with open(export_output_path, "wt") as f:
                for doc in client.iter_jsonl_export(
                    dataset_id=dataset_id,
                    source_stage=stage_enum,
                    max_documents=max_documents,
                    deduplicate=True,
                ):
                    # Remove content field if present
                    if "content" in doc:
                        doc.pop("content")
                    f.write(json.dumps(doc) + "\n")
                    exported_docs += 1
                    total_docs += 1
        else:
            # Use custom export to handle different representation types
            with open(export_output_path, "wt") as f:
                # First discover the right representation type for this dataset
                representation_type = discover_representation_type(
                    client, dataset_id, progress
                )

                if progress and task_id is not None:
                    progress.console.print(
                        f"[bold]Exporting from {dataset_id} using {representation_type} representation[/bold]"
                    )

                # Since the client.iter_jsonl_export requires tokens but many documents
                # in the dataset may not have tokens, we'll read directly from S3
                docs_processed = 0

                # Start by getting document IDs
                for doc_id in client.iter_documents(
                    dataset_id, stage_enum, limit=max_documents
                ):
                    # Retrieve the document
                    document = client.get_document(dataset_id, doc_id, stage_enum)

                    if document:
                        # Get representation content
                        rep_content = document.get_content(stage_enum)

                        if (
                            rep_content
                            and hasattr(rep_content, "documents")
                            and rep_content.documents
                        ):
                            # Process the first document in the representation
                            doc_data = rep_content.documents[0]

                            # Create our own export document
                            export_doc = {
                                "id": doc_data.get("identifier", doc_id),
                                "metadata": {
                                    "source": doc_data.get("source", ""),
                                    "dataset": dataset_id,
                                },
                                "representations": {},  # Will hold all available representations
                            }

                            # Get metadata if available
                            if "metadata" in doc_data:
                                export_doc["metadata"].update(doc_data["metadata"])

                            # Include ALL available representations
                            if "representations" in doc_data:
                                # Go through each representation type
                                for rep_type, rep_data in doc_data[
                                    "representations"
                                ].items():
                                    # Create a new representation entry
                                    export_doc["representations"][rep_type] = {}

                                    # Get content if available
                                    if "content" in rep_data:
                                        export_doc["representations"][rep_type][
                                            "content"
                                        ] = rep_data["content"]

                                    # Get tokens if available
                                    if "tokens" in rep_data:
                                        export_doc["representations"][rep_type][
                                            "tokens"
                                        ] = rep_data.get("tokens", {})

                                # Also set a default text field using the preferred representation type
                                # This ensures backward compatibility
                                if representation_type in doc_data["representations"]:
                                    rep = doc_data["representations"][
                                        representation_type
                                    ]
                                    export_doc["text"] = rep.get("content", "")

                            # Write to the output
                            f.write(json.dumps(export_doc) + "\n")
                            exported_docs += 1
                            docs_processed += 1

                            # Update progress
                            if progress and task_id is not None:
                                progress.update(task_id, completed=docs_processed)

                            # Check if we've reached the limit
                            if max_documents and docs_processed >= max_documents:
                                break

                # Record total docs processed
                total_docs = docs_processed

        # Compress the file if requested and not already handled
        if compress and not output_path.endswith(".gz"):
            import gzip
            import shutil

            # Rename the uncompressed file temporarily
            temp_path = export_output_path + ".temp"
            os.rename(export_output_path, temp_path)

            # Compress the file
            with open(temp_path, "rb") as f_in:
                with gzip.open(output_path, "wb") as f_out:
                    shutil.copyfileobj(f_in, f_out)

            # Remove the temporary file
            os.remove(temp_path)

    # Calculate stats
    duration = time.time() - start_time
    file_size = os.path.getsize(output_path)

    # Prepare result
    result = {
        "dataset_id": dataset_id,
        "output_path": output_path,
        "total_documents": total_docs,
        "exported_documents": exported_docs,
        "filtered_documents": filtered_docs,
        "file_size_bytes": file_size,
        "duration_seconds": duration,
    }

    # Mark task as completed
    if progress and task_id is not None:
        progress.update(task_id, completed=total_docs, total=total_docs)

    return result


def load_filter(filter_path: str) -> Callable[[Dict[str, Any]], bool]:
    """
    Load filter criteria from JSON file.

    Args:
        filter_path: Path to filter JSON file

    Returns:
        Filter function
    """
    with open(filter_path, "r") as f:
        filter_config = json.load(f)

    def filter_func(doc: Dict[str, Any]) -> bool:
        """Filter function to apply to each document."""
        # Include/exclude based on metadata fields
        if "metadata" in filter_config:
            for field, values in filter_config["metadata"].items():
                if field not in doc.get("metadata", {}):
                    return False

                field_value = doc["metadata"][field]

                # Check if field matches any of the allowed values
                if isinstance(values, list) and field_value not in values:
                    return False
                # Check if field matches regex pattern
                elif isinstance(values, str) and values.startswith("regex:"):
                    import re

                    pattern = values[6:]  # Remove "regex:" prefix
                    if not re.search(pattern, str(field_value)):
                        return False

        # Include/exclude based on token count
        if "token_count" in filter_config:
            tokenizer = filter_config["token_count"].get("tokenizer", "cl100k_base")
            min_tokens = filter_config["token_count"].get("min")
            max_tokens = filter_config["token_count"].get("max")

            # Find token count for the specified tokenizer
            token_count = None
            if "tokens" in doc:
                for tok_info in doc["tokens"]:
                    if tok_info.get("tokenizer") == tokenizer:
                        token_count = len(tok_info.get("tokens", []))
                        break

            if token_count is not None:
                if min_tokens is not None and token_count < min_tokens:
                    return False
                if max_tokens is not None and token_count > max_tokens:
                    return False

        # Include/exclude based on content
        if "content" in filter_config and "content" in doc:
            content = doc["content"]

            # Minimum content length
            min_length = filter_config["content"].get("min_length")
            if min_length is not None and len(content) < min_length:
                return False

            # Maximum content length
            max_length = filter_config["content"].get("max_length")
            if max_length is not None and len(content) > max_length:
                return False

            # Content must contain specific text
            must_contain = filter_config["content"].get("must_contain", [])
            for text in must_contain:
                if text not in content:
                    return False

            # Content must not contain specific text
            must_not_contain = filter_config["content"].get("must_not_contain", [])
            for text in must_not_contain:
                if text in content:
                    return False

        # All filters passed
        return True

    return filter_func


def main() -> None:
    """Main entry point."""
    args = parse_args()
    console = Console()

    try:
        # Initialize client
        client = KL3MClient(verbose=args.verbose)

        # Load filter if specified
        filter_func = None
        if args.filter:
            try:
                filter_func = load_filter(args.filter)
                console.print(f"[bold]Loaded filter from: {args.filter}[/bold]")
            except Exception as e:
                console.print(f"[bold red]Error loading filter: {e}[/bold red]")
                return 1

        # Create output directory
        os.makedirs(args.output_dir, exist_ok=True)

        # Set max_documents using limit if provided and max_documents is not
        max_documents = args.max_documents
        if max_documents is None and args.limit is not None:
            max_documents = args.limit
            console.print(f"[bold]Using limit of {max_documents} documents[/bold]")

        # Get document counts for datasets
        dataset_counts = {}
        with console.status("Getting dataset information..."):
            for dataset_id in args.datasets:
                try:
                    status = client.get_dataset_status(dataset_id)
                    dataset_counts[dataset_id] = status.document_count
                except Exception as e:
                    console.print(
                        f"[bold yellow]Warning: Could not get status for {dataset_id}: {e}[/bold yellow]"
                    )
                    dataset_counts[dataset_id] = None

        # Create progress tracking
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("({task.completed}/{task.total})"),
            TimeElapsedColumn(),
        )

        # Submit export tasks
        results = []
        with progress:
            # Create tasks for tracking
            tasks = {}
            for dataset_id in args.datasets:
                # Set expected count (use max_documents/limit if specified)
                count = max_documents or dataset_counts.get(dataset_id, 1000)
                tasks[dataset_id] = progress.add_task(
                    f"[cyan]Exporting {dataset_id}[/cyan]", total=count
                )

            # Use thread pool for parallel export
            with ThreadPoolExecutor(max_workers=args.workers) as executor:
                futures = []

                for dataset_id in args.datasets:
                    future = executor.submit(
                        export_dataset,
                        client=client,
                        dataset_id=dataset_id,
                        output_dir=args.output_dir,
                        source_stage=args.stage,
                        max_documents=max_documents,
                        compress=args.compress,
                        exclude_content=args.exclude_content,
                        filter_func=filter_func,
                        progress=progress,
                        task_id=tasks[dataset_id],
                    )
                    futures.append(future)

                # Collect results as they complete
                for future in futures:
                    try:
                        result = future.result()
                        results.append(result)
                    except Exception as e:
                        console.print(f"[bold red]Export error: {e}[/bold red]")

        # Display results summary
        if results:
            console.print("\n[bold]Export Summary:[/bold]")

            # Create a Rich Table object
            from rich.table import Table

            table = Table()
            table.add_column("Dataset")
            table.add_column("Exported")
            table.add_column("Filtered", justify="right")
            table.add_column("Size", justify="right")
            table.add_column("Duration", justify="right")

            for result in results:
                table.add_row(
                    result["dataset_id"],
                    f"{result['exported_documents']:,}",
                    f"{result['filtered_documents']:,}",
                    f"{result['file_size_bytes'] / (1024*1024):.2f} MB",
                    f"{result['duration_seconds']:.2f}s",
                )

            console.print(table)

            # Show total stats
            total_exported = sum(r["exported_documents"] for r in results)
            total_filtered = sum(r["filtered_documents"] for r in results)
            total_size = sum(r["file_size_bytes"] for r in results) / (1024 * 1024)

            console.print(
                f"\nTotal exported: [bold]{total_exported:,}[/bold] documents"
            )
            if total_filtered > 0:
                console.print(
                    f"Total filtered: [bold]{total_filtered:,}[/bold] documents"
                )
            console.print(f"Total size: [bold]{total_size:.2f} MB[/bold]")

            # Save summary
            summary_path = os.path.join(args.output_dir, "export_summary.json")
            with open(summary_path, "w") as f:
                json.dump(
                    {
                        "datasets": args.datasets,
                        "results": results,
                        "total_exported": total_exported,
                        "total_filtered": total_filtered,
                        "total_size_bytes": sum(r["file_size_bytes"] for r in results),
                        "timestamp": time.time(),
                    },
                    f,
                    indent=2,
                )

            console.print(f"\nSummary saved to: [bold]{summary_path}[/bold]")

    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
