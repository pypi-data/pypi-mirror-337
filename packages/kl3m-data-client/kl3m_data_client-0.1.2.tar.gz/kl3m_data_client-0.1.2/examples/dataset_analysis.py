#!/usr/bin/env python
"""
Dataset Analysis Example for KL3M Data Client.

This script demonstrates how to analyze dataset statistics including
token counts, document sizes, and metadata across multiple datasets.
"""

# imports
import argparse
import json
import sys
from collections import defaultdict
from typing import Dict, List, Any

# packages
from rich.console import Console
from rich.table import Table
from tokenizers import Tokenizer

# project
from kl3m_data_client import KL3MClient
from kl3m_data_client.models.common import Stage


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Analyze KL3M datasets")
    parser.add_argument(
        "datasets",
        nargs="+",
        help="Dataset IDs to analyze (space-separated)",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=100,
        help="Maximum documents to analyze per dataset",
    )
    parser.add_argument(
        "--tokenizer",
        default="alea-institute/kl3m-004-128k-cased",
        help="Tokenizer to use for token counts",
    )
    parser.add_argument("--output", help="Save results to JSON file")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    return parser.parse_args()


def analyze_dataset(
    client: KL3MClient, dataset_id: str, limit: int, tokenizer: str
) -> Dict[str, Any]:
    """
    Analyze a dataset and collect statistics.

    Args:
        client: KL3M client
        dataset_id: Dataset ID to analyze
        limit: Maximum documents to analyze
        tokenizer: Tokenizer to use for token counts

    Returns:
        Dictionary of analysis results
    """
    console = Console()

    # Get dataset status
    console.print(f"Analyzing dataset: [bold cyan]{dataset_id}[/bold cyan]")

    # Initialize results
    results = {
        "dataset_id": dataset_id,
        "analyzed_documents": 0,
        "token_counts": [],
        "document_sizes": [],
        "mime_types": defaultdict(int),
        "metadata_fields": defaultdict(int),
        "formats": defaultdict(int),
        "document_samples": [],
    }

    # get tokenizer
    tokenizer = Tokenizer.from_pretrained(tokenizer)

    # Analyze documents
    console.print(f"  Processing up to {limit} documents...")

    with console.status("Analyzing..."):
        for i, doc_id in enumerate(
            client.iter_documents(dataset_id, Stage.REPRESENTATIONS, limit=limit)
        ):
            document = client.get_document(dataset_id, doc_id, Stage.REPRESENTATIONS)
            document_mime_types = (
                document.get_representation().get_available_mime_types()
            )

            # increment mime type data
            if document_mime_types:
                # Count MIME types
                for mime_type in document_mime_types:
                    results["mime_types"][mime_type] += 1

            if "text/markdown" in document_mime_types:
                # Get the content of the document
                content = document.get_representation().get_content("text/markdown")

            elif "text/plain" in document_mime_types:
                # Fallback to plain text if markdown is not available
                content = document.get_representation().get_content("text/plain")
            else:
                continue

            # tokenize with desired tokenizer and add to counts
            token_count = len(tokenizer.encode(content).ids)
            results["token_counts"].append(token_count)
            results["document_sizes"].append(len(content))
            results["analyzed_documents"] += 1

    # Convert defaultdicts to regular dicts for JSON serialization
    results["mime_types"] = dict(results["mime_types"])

    return results


def display_results(results: List[Dict[str, Any]]) -> None:
    """
    Display analysis results in a formatted table.

    Args:
        results: List of dataset analysis results
    """
    console = Console()

    # Create summary table
    table = Table(title="Dataset Analysis Summary")
    table.add_column("Dataset", style="cyan")
    table.add_column("Analyzed", justify="right")
    table.add_column("Avg Tokens", justify="right")
    table.add_column("Avg Size (bytes)", justify="right")
    table.add_column("MIME Types", justify="right")

    for result in results:
        # Calculate statistics
        avg_tokens = "N/A"
        if result["token_counts"]:
            avg_tokens = (
                f"{sum(result['token_counts']) / len(result['token_counts']):,.1f}"
            )

        avg_size = "N/A"
        if result["document_sizes"]:
            avg_size = (
                f"{sum(result['document_sizes']) / len(result['document_sizes']):,.1f}"
            )

        mime_types = len(result["mime_types"])

        table.add_row(
            result["dataset_id"],
            f"{result['analyzed_documents']:,}",
            avg_tokens,
            avg_size,
            str(mime_types),
        )

    console.print(table)

    # Display detailed information for each dataset
    for result in results:
        console.print(f"\n[bold cyan]Dataset: {result['dataset_id']}[/bold cyan]")

        # Show MIME types
        console.print("\n[bold]MIME Types:[/bold]")
        mime_table = Table("MIME Type", "Count", "Percentage")
        for mime_type, count in sorted(
            result["mime_types"].items(), key=lambda x: x[1], reverse=True
        ):
            percentage = count / result["analyzed_documents"] * 100
            mime_table.add_row(mime_type, str(count), f"{percentage:.1f}%")
        console.print(mime_table)

        # Show token count distribution if available
        if result["token_counts"]:
            token_counts = sorted(result["token_counts"])
            console.print("\n[bold]Token Count Distribution:[/bold]")
            console.print(f"  Min: {min(token_counts):,}")
            console.print(f"  Max: {max(token_counts):,}")
            console.print(f"  Avg: {sum(token_counts) / len(token_counts):,.1f}")

            # Simple percentile calculation
            percentiles = [10, 25, 50, 75, 90]
            for p in percentiles:
                idx = int((p / 100) * len(token_counts))
                console.print(f"  P{p}: {token_counts[idx]:,}")


def main() -> None:
    """Main entry point."""
    args = parse_args()

    try:
        # Initialize client
        client = KL3MClient(verbose=args.verbose)

        # Analyze each dataset
        results = []
        for dataset_id in args.datasets:
            try:
                dataset_results = analyze_dataset(
                    client, dataset_id, args.limit, args.tokenizer
                )
                results.append(dataset_results)
            except Exception as e:
                Console().print(
                    f"[bold red]Error analyzing dataset {dataset_id}: {e}[/bold red]"
                )

        # Display results
        if results:
            display_results(results)

            # Save results if requested
            if args.output:
                with open(args.output, "w") as f:
                    json.dump(results, f, indent=2)
                Console().print(f"\nResults saved to: [bold]{args.output}[/bold]")
        else:
            Console().print(
                "[bold red]No dataset analysis results to display[/bold red]"
            )
            return 1

    except Exception as e:
        Console().print(f"[bold red]Error: {e}[/bold red]")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
