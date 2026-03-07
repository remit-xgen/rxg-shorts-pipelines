"""
Google Trends Analyzer
Fetches trending search keywords from Google Trends
"""

from pytrends.request import TrendReq
from logging.logger import logger


class GoogleTrends:

    def __init__(self, region="US", limit=10):

        self.region = region
        self.limit = limit

        self.pytrends = TrendReq(
            hl="en-US",
            tz=360
        )


    def get_trending(self):

        """
        Get trending searches from Google Trends
        """

        try:

            logger.info("Fetching Google trending searches")

            trending = self.pytrends.trending_searches(
                pn=self.region.lower()
            )

            keywords = trending[0].tolist()

            keywords = keywords[:self.limit]

            logger.info(f"Found {len(keywords)} trending keywords")

            return keywords

        except Exception as e:

            logger.error(f"Google Trends fetch failed: {e}")

            return []