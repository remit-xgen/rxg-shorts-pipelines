"""
Transcription Module
Uses Whisper to convert speech to text
Optimized for Colab Free
"""

import os

from models.model_manager import model_manager
from logging.logger import logger


class Transcription:

    def __init__(self):

        try:

            self.model = model_manager.get_model("whisper")

        except Exception as e:

            logger.error(
                f"Failed to load Whisper model: {e}"
            )

            self.model = None


    def run(self, audio_path):

        """
        Returns transcript segments

        [
            {
                "start": float,
                "end": float,
                "text": str
            }
        ]
        """

        if not self.model:

            logger.error(
                "Whisper model not available"
            )

            return []

        if not os.path.exists(audio_path):

            logger.error(
                f"Audio file not found: {audio_path}"
            )

            return []

        try:

            logger.info(
                f"Starting transcription: {audio_path}"
            )

            result = self.model.transcribe(
                audio_path,
                fp16=False
            )

            segments = []

            for segment in result.get("segments", []):

                segments.append({

                    "start": float(
                        segment.get("start", 0)
                    ),

                    "end": float(
                        segment.get("end", 0)
                    ),

                    "text": segment.get(
                        "text",
                        ""
                    ).strip()
                })

            logger.info(
                f"Transcription segments: {len(segments)}"
            )

            return segments

        except Exception as e:

            logger.error(
                f"Transcription failed: {e}"
            )

            return []