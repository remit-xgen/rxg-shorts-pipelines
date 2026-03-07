"""
Audio Extractor
Extract audio from video files
"""

import os
from moviepy.editor import VideoFileClip
from logging.logger import logger
import config


class AudioExtractor:

    def __init__(self):
        os.makedirs(config.AUDIO_DIR, exist_ok=True)

    def extract(self, video_path):

        """
        Extract audio from video
        """

        try:

            video_name = os.path.basename(video_path).split(".")[0]

            audio_path = os.path.join(
                config.AUDIO_DIR,
                f"{video_name}.wav"
            )

            logger.info(f"Extracting audio from {video_path}")

            video = VideoFileClip(video_path)
            video.audio.write_audiofile(audio_path)

            logger.info(f"Audio saved: {audio_path}")

            return audio_path

        except Exception as e:

            logger.error(f"Audio extraction failed: {e}")
            return None
