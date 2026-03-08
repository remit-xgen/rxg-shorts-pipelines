"""
Transcription Module
Uses Whisper to convert speech to text
"""

import os
from models.model_manager import model_manager
from logging.logger import logger


class Transcription:

    def __init__(self):

        # Load whisper model from singleton model manager
        try:
            self.model = model_manager.get_model("whisper")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
            self.model = None


    def run(self, audio_path):

        """
        Transcribe audio file using Whisper
        Returns list of segments:
        [
            {start: float, end: float, text: str}
        ]
        """

        if not self.model:
            logger.error("Whisper model not available")
            return []

        if not os.path.exists(audio_path):
            logger.error(f"Audio file not found: {audio_path}")
            return []

        try:

            logger.info(f"Starting transcription: {audio_path}")

            result = self.model.transcribe(audio_path)

            if not result or "segments" not in result:
                logger.warning("No transcription segments returned")
                return []

            segments = []

            for segment in result["segments"]:

                segments.append({
                    "start": segment.get("start", 0),
                    "end": segment.get("end", 0),
                    "text": segment.get("text", "").strip()
                })

            logger.info(f"Transcription completed: {len(segments)} segments")

            return segments

        except Exception as e:

            logger.error(f"Transcription failed: {e}")
            return []