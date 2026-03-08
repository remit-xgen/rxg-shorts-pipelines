"""
YouTube Uploader
Handles uploading Shorts to YouTube
Compatible with PipelineOrchestrator
"""

import os
import time

from logging.logger import logger

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

CLIENT_SECRET_FILE = "/content/drive/MyDrive/rxg_pipeline/client_secret.json"
TOKEN_FILE = "/content/drive/MyDrive/rxg_pipeline/token.json"


class YouTubeUploader:

    def __init__(self, token_file=TOKEN_FILE):

        self.token_file = token_file
        self.youtube = self._authenticate()


    def _authenticate(self):

        try:

            if not os.path.exists(self.token_file):

                logger.error("YouTube token.json not found")
                return None

            creds = Credentials.from_authorized_user_file(
                self.token_file,
                SCOPES
            )

            if creds.expired and creds.refresh_token:

                logger.info("Refreshing YouTube token")

                creds.refresh(Request())

            youtube = build(
                "youtube",
                "v3",
                credentials=creds
            )

            logger.info("YouTube authentication successful")

            return youtube

        except Exception as e:

            logger.error(f"YouTube authentication failed: {e}")
            return None


    def upload_video(
        self,
        video_path,
        caption=None,
        privacy="public"
    ):

        try:

            if not self.youtube:

                logger.error("YouTube client not initialized")
                return None

            if not os.path.exists(video_path):

                logger.error(f"Video not found: {video_path}")
                return None

            logger.info(f"Uploading video: {video_path}")

            title = self._generate_title(caption)

            description = self._generate_description(caption)

            tags = self._extract_tags(caption)

            request_body = {

                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags,
                    "categoryId": "22"
                },

                "status": {
                    "privacyStatus": privacy,
                    "selfDeclaredMadeForKids": False
                }

            }

            media = MediaFileUpload(
                video_path,
                chunksize=-1,
                resumable=True
            )

            request = self.youtube.videos().insert(
                part="snippet,status",
                body=request_body,
                media_body=media
            )

            response = None

            while response is None:

                status, response = request.next_chunk()

                if status:

                    progress = int(status.progress() * 100)

                    logger.info(f"Upload progress: {progress}%")

                    time.sleep(1)

            logger.info("YouTube upload completed")

            return response

        except Exception as e:

            logger.error(f"YouTube upload failed: {e}")

            return None


    def _generate_title(self, caption):

        if not caption:
            return "Viral Short"

        title = caption.split("\n")[0]

        if len(title) > 90:
            title = title[:90]

        return title


    def _generate_description(self, caption):

        if not caption:
            return "#shorts"

        return f"{caption}\n\n#shorts"


    def _extract_tags(self, caption):

        if not caption:
            return []

        tags = []

        for word in caption.split():

            if word.startswith("#"):

                tag = word.replace("#", "")

                if tag not in tags:
                    tags.append(tag)

        return tags