"""
Trend Selector
Selects top trending keywords after ranking
"""

from logging.logger import logger


class TrendSelector:

    def __init__(self, limit=5):

        self.limit = limit


    def select(self, ranked_keywords):

        """
        Select top ranked keywords
        """

        try:

            logger.info("Selecting top trending keywords")

            selected = []
            seen = set()

            for item in ranked_keywords:

                keyword = item.get("keyword")

                if not keyword:
                    continue

                if keyword in seen:
                    continue

                selected.append(keyword)
                seen.add(keyword)

                if len(selected) >= self.limit:
                    break

            logger.info(f"Selected {len(selected)} trending keywords")

            return selected

        except Exception as e:

            logger.error(f"Trend selection failed: {e}")

            return []