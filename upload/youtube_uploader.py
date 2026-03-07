"""
YouTube Shorts Uploader
"""

import os

from logging.logger import logger

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class YouTubeUploader:

    def __init__(self, youtube_service):

        self.youtube = youtube_service

    def upload_short(self, video_path, title, description, tags=None):

        try:

            logger.info(f"Uploading video: {video_path}")

            body = {
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags or [],
                    "categoryId": "22"
                },
                "status": {
                    "privacyStatus": "public"
                }
            }

            media = MediaFileUpload(
                video_path,
                chunksize=-1,
                resumable=True
            )

            request = self.youtube.videos().insert(
                part="snippet,status",
                body=body,
                media_body=media
            )

            response = request.execute()

            video_id = response["id"]

            logger.info(f"Upload successful: {video_id}")

            return video_id

        except Exception as e:

            logger.error(f"YouTube upload failed: {e}")
            return None
