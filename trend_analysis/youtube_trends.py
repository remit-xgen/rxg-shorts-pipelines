"""
YouTube Trend Analysis
Fetch trending videos from YouTube
"""

from yt_dlp import YoutubeDL
from logging.logger import logger


class YouTubeTrends:

    def __init__(self, max_results=10):
        self.max_results = max_results

    def fetch_trending(self):
        """
        Fetch trending YouTube videos
        """

        logger.info("Fetching trending YouTube videos")

        url = "https://www.youtube.com/feed/trending"

        ydl_opts = {
            "quiet": True,
            "extract_flat": True
        }

        videos = []

        with YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=False)

            for entry in info["entries"][:self.max_results]:

                video_data = {
                    "id": entry["id"],
                    "title": entry["title"],
                    "url": f"https://www.youtube.com/watch?v={entry['id']}"
                }

                videos.append(video_data)

        logger.info(f"Fetched {len(videos)} trending videos")

        return videos
