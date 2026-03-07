"""
Parallel Processor
Handles parallel execution of tasks
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from logging.logger import logger


class ParallelProcessor:

    def __init__(self, max_workers=2):
        self.max_workers = max_workers

    def run(self, items, task_function):
        """
        Run tasks in parallel
        """

        results = []

        logger.info(f"Starting parallel processing with {self.max_workers} workers")

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:

            futures = [executor.submit(task_function, item) for item in items]

            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logger.error(f"Parallel task failed: {e}")

        return results
