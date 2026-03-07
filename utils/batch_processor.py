"""
Batch Processor
Handles splitting tasks into manageable batches
"""

from logging.logger import logger


class BatchProcessor:

    def __init__(self, batch_size=2):
        self.batch_size = batch_size

    def create_batches(self, items):
        """
        Split items into batches
        """
        batches = []

        for i in range(0, len(items), self.batch_size):
            batch = items[i:i + self.batch_size]
            batches.append(batch)

        logger.info(f"Created {len(batches)} batches")

        return batches

    def process_batches(self, items, process_function):
        """
        Process items batch by batch
        """
        batches = self.create_batches(items)

        results = []

        for i, batch in enumerate(batches):

            logger.info(f"Processing batch {i+1}/{len(batches)}")

            for item in batch:
                result = process_function(item)
                results.append(result)

        return results
