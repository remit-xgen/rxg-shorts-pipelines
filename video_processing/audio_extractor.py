"""
Audio Extractor
Extract audio from video files
"""

import os
from moviepy.editor import VideoFileClip
from logging.logger import logger


class AudioExtractor:

    def __init__(self):

        self.temp_dir = "temp"
        os.makedirs(self.temp_dir, exist_ok=True)


    def extract(self, video_path):

        """
        Extract audio from video
        """

        try:

            video_name = os.path.basename(video_path).split(".")[0]

            audio_path = os.path.join(
                self.temp_dir,
                f"{video_name}.wav"
            )

            logger.info(f"Extracting audio from {video_path}")

            video = VideoFileClip(video_path)

            video.audio.write_audiofile(
                audio_path,
                logger=None
            )

            video.close()

            logger.info(f"Audio saved: {audio_path}")

            return audio_path

        except Exception as e:

            logger.error(f"Audio extraction failed: {e}")
            return None