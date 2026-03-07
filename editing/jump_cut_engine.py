"""
Jump Cut Engine
Apply fast paced jump cuts to clips
"""

import os
import subprocess

from logging.logger import logger


class JumpCutEngine:

    def __init__(self):

        self.output_dir = "workspace/jumpcut_clips"
        os.makedirs(self.output_dir, exist_ok=True)

        self.temp_dir = "workspace/temp_cuts"
        os.makedirs(self.temp_dir, exist_ok=True)

    def apply(self, clips):

        try:

            logger.info("Applying jump cuts")

            processed = []

            for i, clip in enumerate(clips):

                video_path = clip["path"]
                cuts = clip.get("cuts", [])

                if len(cuts) < 2:
                    processed.append(clip)
                    continue

                cut_files = []

                for j in range(len(cuts) - 1):

                    start = cuts[j]
                    end = cuts[j + 1]
                    duration = end - start

                    cut_path = os.path.join(
                        self.temp_dir,
                        f"cut_{i}_{j}.mp4"
                    )

                    command = [
                        "ffmpeg",
                        "-y",
                        "-ss", str(start),
                        "-i", video_path,
                        "-t", str(duration),
                        "-c", "copy",
                        cut_path
                    ]

                    subprocess.run(
                        command,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL
                    )

                    cut_files.append(cut_path)

                list_file = os.path.join(
                    self.temp_dir,
                    f"list_{i}.txt"
                )

                with open(list_file, "w") as f:
                    for path in cut_files:
                        f.write(f"file '{path}'\n")

                output_path = os.path.join(
                    self.output_dir,
                    f"jumpcut_{i}.mp4"
                )

                command = [
                    "ffmpeg",
                    "-y",
                    "-f", "concat",
                    "-safe", "0",
                    "-i", list_file,
                    "-c", "copy",
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

            logger.info("Jump cuts completed")

            return processed

        except Exception as e:

            logger.error(f"Jump cut engine failed: {e}")
            return []
