"""
Clip Selector
Select best non-overlapping clips
"""

from logging.logger import logger


class ClipSelector:

    def __init__(self):

        self.max_clips = 3
        self.min_gap = 3

    def select(self, ranked_clips):

        try:

            logger.info("Selecting best clips")

            selected = []

            for clip in ranked_clips:

                if len(selected) >= self.max_clips:
                    break

                overlap = False

                for s in selected:

                    if not (
                        clip["end"] + self.min_gap < s["start"] or
                        clip["start"] - self.min_gap > s["end"]
                    ):
                        overlap = True
                        break

                if not overlap:
                    selected.append(clip)

            logger.info(f"Final clips selected: {len(selected)}")

            return selected

        except Exception as e:

            logger.error(f"Clip selection failed: {e}")
            return []
