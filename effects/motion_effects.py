"""
Motion Effects
Adds subtle camera movement to make clips more dynamic
"""

import os
import subprocess
import random

from logging.logger import logger


class MotionEffects:

    def __init__(self):

        self.output_dir = "workspace/motion_clips"
        os.makedirs(self.output_dir, exist_ok=True)

    def apply(self, clips):

        try:

            logger.info("Applying motion effects")

            processed = []

            for i, clip in enumerate(clips):

                video_path = clip["path"]

                output_path = os.path.join(
                    self.output_dir,
                    f"motion_{i}.mp4"
                )

                direction = random.choice([
                    "left",
                    "right",
                    "up",
                    "down"
                ])

                if direction == "left":
                    motion_filter = "crop=iw*0.95:ih*0.95:x='(iw-iw*0.95)*(t/5)':y=0"

                elif direction == "right":
                    motion_filter = "crop=iw*0.95:ih*0.95:x='(iw-iw*0.95)*(1-t/5)':y=0"

                elif direction == "up":
                    motion_filter = "crop=iw*0.95:ih*0.95:x=0:y='(ih-ih*0.95)*(t/5)'"

                else:
                    motion_filter = "crop=iw*0.95:ih*0.95:x=0:y='(ih-ih*0.95)*(1-t/5)'"

                command = [
                    "ffmpeg",
                    "-y",
                    "-i", video_path,
                    "-vf", motion_filter,
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

            logger.info("Motion effects applied")

            return processed

        except Exception as e:

            logger.error(f"Motion effects failed: {e}")
            return []
