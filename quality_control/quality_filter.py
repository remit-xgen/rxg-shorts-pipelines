"""
Quality Filter
Filters clips based on quality metrics before export
"""

from logging.logger import logger


class QualityFilter:

    def __init__(
        self,
        min_duration=5,
        max_duration=60,
        min_score=1.0,
        min_hooks=1
    ):

        self.min_duration = min_duration
        self.max_duration = max_duration
        self.min_score = min_score
        self.min_hooks = min_hooks


    def filter(self, clips):

        """
        Filter clips based on quality thresholds
        """

        try:

            logger.info("Running quality filter")

            passed = []

            for clip in clips:

                duration = clip.get("duration", 0)
                score = clip.get("score", 0)
                hooks = clip.get("hooks", [])

                if duration < self.min_duration:
                    continue

                if duration > self.max_duration:
                    continue

                if score < self.min_score:
                    continue

                if len(hooks) < self.min_hooks:
                    continue

                passed.append(clip)

            logger.info(f"{len(passed)} clips passed quality filter")

            return passed

        except Exception as e:

            logger.error(f"Quality filter failed: {e}")

            return []
