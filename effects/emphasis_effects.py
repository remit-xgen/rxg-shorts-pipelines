"""
Emphasis Effects
Adds visual punch to highlight important moments
"""

import os
import subprocess
import random

from logging.logger import logger


class EmphasisEffects:

    def __init__(self):

        self.output_dir = "workspace/emphasis_clips"
        os.makedirs(self.output_dir, exist_ok=True)

    def apply(self, clips):

        try:

            logger.info("Applying emphasis effects")

            processed = []

            for i, clip in enumerate(clips):

                video_path = clip["path"]

                output_path = os.path.join(
                    self.output_dir,
                    f"emphasis_{i}.mp4"
                )

                effect = random.choice([
                    "brightness",
                    "shake"
                ])

                if effect == "brightness":

                    filter_effect = "eq=brightness=0.06:saturation=1.2"

                else:

                    # micro shake effect
                    filter_effect = (
                        "crop=iw*0.98:ih*0.98:"
                        "x='if(gte(mod(t,0.1),0.05),2,0)':"
                        "y='if(gte(mod(t,0.1),0.05),2,0)'"
                    )

                command = [
                    "ffmpeg",
                    "-y",
                    "-i", video_path,
                    "-vf", filter_effect,
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

            logger.info("Emphasis effects applied")

            return processed

        except Exception as e:

            logger.error(f"Emphasis effects failed: {e}")
            return []
