"""
Parallel processing utilities for the KL3M data client.
"""

import logging
import time
import traceback
from typing import List, Optional, Callable, TypeVar, Generic, Tuple
from concurrent.futures import ThreadPoolExecutor

from rich.progress import Progress, TaskID

T = TypeVar("T")
R = TypeVar("R")

logger = logging.getLogger("kl3m_data_client")


class ParallelExecutor(Generic[T, R]):
    """
    Utility class for executing tasks in parallel with progress tracking.
    """

    def __init__(
        self,
        worker_fn: Callable[[T], R],
        max_workers: int = 10,
        progress: Optional[Progress] = None,
        task_id: Optional[TaskID] = None,
        description: str = "Processing",
    ):
        """
        Initialize a parallel executor.

        Args:
            worker_fn: The worker function to execute on each item.
            max_workers: Maximum number of worker threads.
            progress: Optional Progress object for tracking progress.
            task_id: Optional task ID for the progress bar.
            description: Description for the progress bar.
        """
        self.worker_fn = worker_fn
        self.max_workers = max_workers
        self.progress = progress
        self.task_id = task_id
        self.description = description

    def process_batch(self, items: List[T]) -> Tuple[List[R], List[Exception]]:
        """
        Process a batch of items in parallel.

        Args:
            items: List of items to process.

        Returns:
            Tuple of (successful results, exceptions).
        """
        if not items:
            return [], []

        start_time = time.time()
        successful_results = []
        exceptions = []

        # Create the executor
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all tasks
            future_to_item = {}
            for item in items:
                future = executor.submit(self._execute_worker, item)
                future_to_item[future] = item

            # Create progress tracking if needed
            task_id: Optional[TaskID] = self.task_id
            if self.progress is not None and task_id is None:
                task_id = self.progress.add_task(self.description, total=len(items))

            # Process results as they complete
            for i, future in enumerate(future_to_item):
                item = future_to_item[future]
                try:
                    result = future.result()
                    successful_results.append(result)
                except Exception as e:
                    logger.error("Error processing item %s: %s", item, e)
                    logger.debug(traceback.format_exc())
                    exceptions.append(e)

                # Update progress if available
                if self.progress is not None and task_id is not None:
                    self.progress.update(task_id, completed=i + 1)

            # Ensure progress bar is complete
            if self.progress is not None and task_id is not None:
                self.progress.update(task_id, completed=len(items))

        duration = time.time() - start_time
        rate = len(successful_results) / duration if duration > 0 else 0
        logger.info(
            "Processed %d items in %.2f seconds (%.2f items/sec). Errors: %d",
            len(successful_results),
            duration,
            rate,
            len(exceptions),
        )

        return successful_results, exceptions

    def _execute_worker(self, item: T) -> R:
        """
        Execute the worker function with error handling.

        Args:
            item: The item to process.

        Returns:
            The result of the worker function.

        Raises:
            Exception: Any exception from the worker function.
        """
        try:
            return self.worker_fn(item)
        except Exception as e:
            logger.error("Error in worker function: %s", e)
            raise
