"""
Shorts Exporter
Exports final processed clips into Shorts-ready format
"""

import os
import uuid
import subprocess

from logging.logger import logger


class ShortsExporter:

    def __init__(self, output_dir="exports"):

        self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)


    def export(self, input_video):

        """
        Export video into Shorts-ready format
        """

        try:

            logger.info("Exporting final shorts video")

            output_file = os.path.join(
                self.output_dir,
                f"short_{uuid.uuid4().hex}.mp4"
            )

            command = [
                "ffmpeg",
                "-y",
                "-i", input_video,
                "-vf", "scale=1080:1920",
                "-c:v", "libx264",
                "-preset", "fast",
                "-crf", "23",
                "-c:a", "aac",
                "-b:a", "128k",
                output_file
            ]

            subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            logger.info(f"Shorts exported: {output_file}")

            return output_file

        except Exception as e:

            logger.error(f"Shorts export failed: {e}")

            return input_video
