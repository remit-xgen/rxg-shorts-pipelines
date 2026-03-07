"""
YouTube Uploader
Handles uploading Shorts to YouTube
"""

import os

from logging.logger import logger

from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle


SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]


class YouTubeUploader:

    def __init__(self, client_secret_file="client_secret.json"):

        self.client_secret_file = client_secret_file
        self.youtube = self._authenticate()


    def _authenticate(self):

        creds = None

        if os.path.exists("token.pickle"):

            with open("token.pickle", "rb") as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:

            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())

            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secret_file,
                    SCOPES
                )

                creds = flow.run_local_server(port=0)

            with open("token.pickle", "wb") as token:
                pickle.dump(creds, token)

        return build("youtube", "v3", credentials=creds)


    def upload_video(
        self,
        video_path,
        title,
        description,
        tags=None,
        privacy="public"
    ):

        try:

            logger.info(f"Uploading video to YouTube: {video_path}")

            request_body = {

                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": tags if tags else [],
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

                    logger.info(
                        f"Upload progress: {int(status.progress() * 100)}%"
                    )

            logger.info("Upload completed")

            return response

        except Exception as e:

            logger.error(f"YouTube upload failed: {e}")

            return None
