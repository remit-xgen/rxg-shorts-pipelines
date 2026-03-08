"""
Subtitle Engine
Generates and embeds subtitles into clips with safe wrapping
"""

import os
import subprocess
import textwrap

from logging.logger import logger
from subtitles.subtitle_styles import SubtitleStyles


class SubtitleEngine:

    def __init__(self):

        self.subtitle_dir = "workspace/subtitles"
        self.output_dir = "workspace/subtitled_clips"

        os.makedirs(self.subtitle_dir, exist_ok=True)
        os.makedirs(self.output_dir, exist_ok=True)

        self.style = SubtitleStyles.tiktok()

        # wrapping configuration
        self.max_chars_per_line = 40
        self.max_lines = 2

    def apply(self, clips, transcript):

        try:

            logger.info("Generating subtitles")

            processed = []

            for i, clip in enumerate(clips):

                video_path = clip["path"]
                start = clip.get("start", 0)
                end = clip.get("end", 999999)

                clip_transcript = self._filter_transcript(
                    transcript,
                    start,
                    end
                )

                if not clip_transcript:
                    logger.warning("No transcript for clip")
                    continue

                srt_path = os.path.join(
                    self.subtitle_dir,
                    f"subtitle_{i}.srt"
                )

                output_path = os.path.join(
                    self.output_dir,
                    f"subtitled_{i}.mp4"
                )

                self._generate_srt(
                    clip_transcript,
                    srt_path,
                    start
                )

                # escape path for ffmpeg
                escaped = srt_path.replace("\\", "/").replace(":", "\\:")

                command = [
                    "ffmpeg",
                    "-y",
                    "-i", video_path,
                    "-vf", f"subtitles='{escaped}'",
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

    def _filter_transcript(self, transcript, start, end):

        filtered = []

        for seg in transcript:

            if seg["end"] < start:
                continue

            if seg["start"] > end:
                break

            filtered.append(seg)

        return filtered

    def _generate_srt(self, transcript, path, clip_start):

        with open(path, "w", encoding="utf-8") as f:

            index = 1

            for segment in transcript:

                start = segment["start"] - clip_start
                end = segment["end"] - clip_start

                if end <= 0:
                    continue

                start = max(start, 0)

                text = self._clean_text(segment["text"])

                lines = self._wrap_text(text)

                subtitle_text = "\n".join(lines)

                start_time = self._format_time(start)
                end_time = self._format_time(end)

                f.write(f"{index}\n")
                f.write(f"{start_time} --> {end_time}\n")
                f.write(f"{subtitle_text}\n\n")

                index += 1

    def _wrap_text(self, text):

        wrapped = textwrap.wrap(
            text,
            width=self.max_chars_per_line
        )

        if len(wrapped) <= self.max_lines:
            return wrapped

        lines = []
        buffer = ""

        for word in text.split():

            candidate = f"{buffer} {word}".strip()

            if len(candidate) <= self.max_chars_per_line:
                buffer = candidate
            else:
                lines.append(buffer)
                buffer = word

        if buffer:
            lines.append(buffer)

        return lines[:self.max_lines]

    def _clean_text(self, text):

        text = text.strip()

        # remove double spaces
        text = " ".join(text.split())

        # optional stylistic tweaks
        text = text.replace(" i ", " I ")

        return text

    def _format_time(self, seconds):

        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)

        return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"