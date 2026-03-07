"""
Zoom Effects
Adds dynamic zoom to clips to increase engagement
"""

import os
import subprocess

from logging.logger import logger


class ZoomEffects:

    def __init__(self):

        self.output_dir = "workspace/zoom_clips"
        os.makedirs(self.output_dir, exist_ok=True)

    def apply(self, clips):

        try:

            logger.info("Applying zoom effects")

            processed = []

            for i, clip in enumerate(clips):

                video_path = clip["path"]

                output_path = os.path.join(
                    self.output_dir,
                    f"zoom_{i}.mp4"
                )

                zoom_filter = (
                    "scale=iw*1.1:ih*1.1,"
                    "crop=iw/1.1:ih/1.1"
                )

                command = [
                    "ffmpeg",
                    "-y",
                    "-i", video_path,
                    "-vf", zoom_filter,
                    "-c:a", "copy",
                    output_path
                ]

                subprocess.run(
                    command,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

                processed.append({
                    "path": output_path,
                    "score": clip["score"]
                })

            logger.info("Zoom effects applied")

            return processed

        except Exception as e:

            logger.error(f"Zoom effects failed: {e}")
            return []
