"""
Whisper Model Manager
Loads Whisper model once and reuse it
"""

import whisper
from logging.logger import logger


class WhisperModelManager:

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            logger.info("Loading Whisper model...")

            cls._model = whisper.load_model("base")

            logger.info("Whisper model loaded")

        return cls._model