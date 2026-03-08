"""
YouTube Search
Viral Video Discovery Engine
Searches YouTube for candidate videos using keywords
"""

import time
import yt_dlp

from logging.logger import logger


class YouTubeSearch:

    def __init__(self, max_results=10, retries=3):

        self.max_results = max_results
        self.retries = retries

        self.ydl_opts = {
            "quiet": True,
            "skip_download": True,
            "extract_flat": True
        }


    def search(self, keywords):

        """
        Search YouTube using a list of keywords
        """

        try:

            logger.info("Starting YouTube discovery")

            results = []
            seen_urls = set()

            for keyword in keywords:

                logger.info(f"Searching keyword: {keyword}")

                search_query = f"ytsearch{self.max_results}:{keyword}"

                search_results = self._search_with_retry(search_query)

                if not search_results:
                    continue

                if "entries" not in search_results:
                    continue

                for entry in search_results["entries"]:

                    if not entry:
                        continue

                    video_url = entry.get("url") or entry.get("webpage_url")

                    if not video_url:
                        continue

                    if video_url in seen_urls:
                        continue

                    duration = entry.get("duration", 0)

                    # prefer shorter videos for shorts pipeline
                    if duration and duration > 1200:
                        continue

                    seen_urls.add(video_url)

                    results.append({
                        "url": video_url,
                        "title": entry.get("title", ""),
                        "duration": duration,
                        "views": entry.get("view_count", 0)
                    })

            logger.info(f"Discovered {len(results)} candidate videos")

            return results

        except Exception as e:

            logger.error(f"YouTube search failed: {e}")

            return []


    def _search_with_retry(self, search_query):

        """
        Execute yt-dlp search with retry + exponential backoff
        """

        for attempt in range(self.retries):

            try:

                with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:

                    return ydl.extract_info(
                        search_query,
                        download=False
                    )

            except Exception as e:

                logger.warning(
                    f"YouTube search retry {attempt+1}/{self.retries}: {e}"
                )

                time.sleep(2 ** attempt)

        logger.error("YouTube search failed after retries")

        return None