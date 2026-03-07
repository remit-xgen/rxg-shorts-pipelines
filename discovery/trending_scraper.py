"""
Trending Scraper
Scrapes trending videos from YouTube trending page
"""

import requests
from bs4 import BeautifulSoup

from logging.logger import logger


class TrendingScraper:

    def __init__(self, region="US", max_results=20):

        self.region = region
        self.max_results = max_results


    def scrape(self):

        """
        Scrape trending videos from YouTube
        """

        try:

            logger.info("Scraping YouTube trending videos")

            url = f"https://www.youtube.com/feed/trending?gl={self.region}"

            headers = {
                "User-Agent": "Mozilla/5.0"
            }

            response = requests.get(url, headers=headers)

            if response.status_code != 200:

                logger.error("Failed to fetch trending page")

                return []

            soup = BeautifulSoup(response.text, "html.parser")

            video_links = []

            for link in soup.find_all("a", href=True):

                href = link["href"]

                if "/watch?v=" in href:

                    video_url = f"https://www.youtube.com{href}"

                    if video_url not in video_links:

                        video_links.append(video_url)

                if len(video_links) >= self.max_results:

                    break

            logger.info(f"Found {len(video_links)} trending videos")

            return video_links

        except Exception as e:

            logger.error(f"Trending scraper failed: {e}")

            return []