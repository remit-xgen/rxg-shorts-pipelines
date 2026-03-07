"""
YouTube Downloader
Download videos using yt-dlp
"""

import os
from yt_dlp import YoutubeDL
from logging.logger import logger
import config


class YouTubeDownloader:

    def __init__(self):
        os.makedirs(config.DOWNLOAD_DIR, exist_ok=True)

    def download(self, video):

        """
        Download video from YouTube
        """

        url = video["url"]
        video_id = video["id"]

        logger.info(f"Downloading video: {video_id}")

        output_path = os.path.join(config.DOWNLOAD_DIR, f"{video_id}.mp4")

        ydl_opts = {
            "outtmpl": output_path,
            "format": "mp4",
            "quiet": True
        }

        try:

            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            logger.info(f"Downloaded: {output_path}")

            return output_path

        except Exception as e:

            logger.error(f"Download failed: {e}")
            return None
