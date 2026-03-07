"""
Clip Extractor
Extract clips from original video using timestamps
"""

import os
import subprocess

from logging.logger import logger
from utils.file_manager import FileManager


class ClipExtractor:

    def __init__(self):

        self.output_dir = "workspace/clips"
        os.makedirs(self.output_dir, exist_ok=True)

    def extract(self, video_path, clips):

        try:

            logger.info("Extracting clips from video")

            extracted = []

            for i, clip in enumerate(clips):

                start = clip["start"]
                end = clip["end"]

                duration = end - start

                output_path = os.path.join(
                    self.output_dir,
                    f"clip_{i}.mp4"
                )

                command = [
                    "ffmpeg",
                    "-y",
                    "-ss", str(start),
                    "-i", video_path,
                    "-t", str(duration),
                    "-c", "copy",
                    output_path
                ]

                subprocess.run(
                    command,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

                extracted.append({
                    "path": output_path,
                    "start": start,
                    "end": end,
                    "cuts": clip.get("cuts", []),
                    "score": clip.get("score", 0)
                })

            logger.info(f"{len(extracted)} clips extracted")

            return extracted

        except Exception as e:

            logger.error(f"Clip extraction failed: {e}")
            return []
