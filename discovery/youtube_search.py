"""
YouTube Search
Searches YouTube for videos using keywords
"""

import yt_dlp

from logging.logger import logger


class YouTubeSearch:

    def __init__(self, max_results=10):

        self.max_results = max_results


    def search(self, keywords):

        """
        Search YouTube using a list of keywords
        """

        try:

            logger.info("Searching YouTube videos")

            results = []

            for keyword in keywords:

                logger.info(f"Searching keyword: {keyword}")

                search_query = f"ytsearch{self.max_results}:{keyword}"

                with yt_dlp.YoutubeDL({
                    "quiet": True,
                    "skip_download": True
                }) as ydl:

                    search_results = ydl.extract_info(
                        search_query,
                        download=False
                    )

                if "entries" not in search_results:
                    continue

                for entry in search_results["entries"]:

                    if not entry:
                        continue

                    video_url = entry.get("webpage_url")

                    if video_url:
                        results.append(video_url)

            logger.info(f"Found {len(results)} videos")

            return results

        except Exception as e:

            logger.error(f"YouTube search failed: {e}")

            return []
