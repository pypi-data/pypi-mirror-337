"""
Console utilities for the KL3M data client.
"""

import logging
from typing import Dict, Optional, Union

from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn, TimeElapsedColumn, TimeRemainingColumn
from rich.logging import RichHandler

from kl3m_data_client.models.common import Stage, DatasetStatus, ProcessingResult


def configure_logging(verbose: bool = False, console: Optional[Console] = None) -> None:
    """
    Configure logging for the KL3M data client.

    Args:
        verbose: Whether to enable verbose logging.
        console: Optional Rich console to use for logging.
    """
    level = logging.DEBUG if verbose else logging.INFO

    if console is None:
        console = Console()

    # Configure rich handler
    rich_handler = RichHandler(
        console=console,
        rich_tracebacks=True,
        show_time=True,
        show_path=verbose,
    )

    # Set up root logger
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[rich_handler],
    )

    # Set up kl3m_data_client logger
    logger = logging.getLogger("kl3m_data_client")
    logger.setLevel(level)

    # Adjust boto3 and botocore loggers
    logging.getLogger("boto3").setLevel(logging.WARNING)
    logging.getLogger("botocore").setLevel(logging.WARNING)
    logging.getLogger("s3transfer").setLevel(logging.WARNING)

    logger.debug("Logging configured with verbose=%s", verbose)


def create_dataset_status_table(
    status: Union[DatasetStatus, Dict[str, DatasetStatus]],
) -> Table:
    """
    Create a Rich table to display dataset status.

    Args:
        status: A DatasetStatus object or a dictionary of dataset IDs to DatasetStatus objects.

    Returns:
        A Rich table displaying the dataset status.
    """
    table = Table()

    # Add columns
    table.add_column("Dataset", style="cyan")
    table.add_column("Documents", style="green", justify="right")
    table.add_column("Representations", style="green", justify="right")
    table.add_column("Parquet", style="green", justify="right")
    table.add_column("Missing Rep.", style="red", justify="right")
    table.add_column("Missing Parq.", style="red", justify="right")
    table.add_column("Status", style="blue")

    # Convert single status to dict for consistent handling
    if isinstance(status, DatasetStatus):
        status_dict = {status.dataset_id: status}
    else:
        status_dict = status

    # Add rows
    for dataset_id, ds_status in sorted(status_dict.items()):
        status_text = "✓ Complete" if ds_status.is_complete else "⚠ Incomplete"

        table.add_row(
            dataset_id,
            str(ds_status.document_count),
            str(ds_status.representation_count),
            str(ds_status.parquet_count),
            str(ds_status.missing_representations),
            str(ds_status.missing_parquet),
            status_text,
        )

    return table


def create_processing_result_table(
    dataset_id: str, stage_from: Stage, stage_to: Stage, result: ProcessingResult
) -> Table:
    """
    Create a Rich table to display processing results.

    Args:
        dataset_id: The dataset ID.
        stage_from: The source stage.
        stage_to: The target stage.
        result: The processing result.

    Returns:
        A Rich table displaying the processing results.
    """
    table = Table()

    # Add columns
    table.add_column("Dataset", style="cyan")
    table.add_column("Operation", style="blue")
    table.add_column("Processed", style="green", justify="right")
    table.add_column("Errors", style="red", justify="right")
    table.add_column("Duration (s)", style="magenta", justify="right")
    table.add_column("Rate (docs/s)", style="yellow", justify="right")

    # Operation description
    operation = f"{stage_from.value} → {stage_to.value}"

    # Add row
    table.add_row(
        dataset_id,
        operation,
        str(result.processed_count),
        str(result.error_count),
        f"{result.duration_seconds:.2f}",
        f"{result.docs_per_second:.2f}",
    )

    return table


def create_dataset_list_table(datasets: Dict[str, Dict[Stage, bool]]) -> Table:
    """
    Create a Rich table to display a list of datasets.

    Args:
        datasets: A dictionary mapping dataset IDs to a dictionary of stages to boolean values
                 indicating whether the dataset has data in that stage.

    Returns:
        A Rich table displaying the list of datasets.
    """
    table = Table(title="Available Datasets")

    # Add columns
    table.add_column("Dataset ID", style="cyan")
    table.add_column("Documents", style="green")
    table.add_column("Representations", style="green")
    table.add_column("Parquet", style="green")

    # Add rows
    for dataset_id, stages in sorted(datasets.items()):
        table.add_row(
            dataset_id,
            "✓" if stages.get(Stage.DOCUMENTS, False) else "✗",
            "✓" if stages.get(Stage.REPRESENTATIONS, False) else "✗",
            "✓" if stages.get(Stage.PARQUET, False) else "✗",
        )

    return table


def create_progress_bar() -> Progress:
    """
    Create a Rich progress bar for processing operations.

    Returns:
        A Rich progress bar.
    """
    return Progress(
        "[progress.description]{task.description}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        "[cyan]{task.completed}/{task.total}",
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=Console(),
    )
