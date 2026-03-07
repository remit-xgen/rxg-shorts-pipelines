"""
Subtitle Engine
Generates and embeds subtitles into clips
"""

import os
import subprocess

from logging.logger import logger
from subtitles.subtitle_styles import SubtitleStyles


class SubtitleEngine:

    def __init__(self):

        self.subtitle_dir = "workspace/subtitles"
        self.output_dir = "workspace/subtitled_clips"

        os.makedirs(self.subtitle_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

        self.style = SubtitleStyles.tiktok()

    def apply(self, clips, transcript):

        try:

            logger.info("Generating subtitles")

            processed = []

            for i, clip in enumerate(clips):

                video_path = clip["path"]

                srt_path = os.path.join(
                    self.subtitle_dir,
                    f"subtitle_{i}.srt"
                )

                output_path = os.path.join(
                    self.output_dir,
                    f"subtitled_{i}.mp4"
                )

                self._generate_srt(transcript, srt_path)

                command = [
                    "ffmpeg",
                    "-y",
                    "-i", video_path,
                    "-vf", f"subtitles={srt_path}",
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

            logger.info("Subtitles applied")

            return processed

        except Exception as e:

            logger.error(f"Subtitle generation failed: {e}")
            return []

    def _generate_srt(self, transcript, path):

        with open(path, "w", encoding="utf-8") as f:

            index = 1

            for segment in transcript:

                start = self._format_time(segment["start"])
                end = self._format_time(segment["end"])
                text = segment["text"]

                f.write(f"{index}\n")
                f.write(f"{start} --> {end}\n")
                f.write(f"{text}\n\n")

                index += 1

    def _format_time(self, seconds):

        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)

        return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"
