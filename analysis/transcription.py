"""
Transcription Module
Uses Whisper to convert speech to text
"""

from models.model_manager import model_manager
from logging.logger import logger


class Transcription:

    def __init__(self):
        self.model = model_manager.load_whisper()

    def transcribe(self, audio_path):

        """
        Transcribe audio file using Whisper
        """

        try:

            logger.info(f"Transcribing audio: {audio_path}")

            result = self.model.transcribe(audio_path)

            segments = []

            for segment in result["segments"]:

                segments.append({
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"]
                })

            logger.info(f"Transcription completed: {len(segments)} segments")

            return segments

        except Exception as e:

            logger.error(f"Transcription failed: {e}")
            return []
