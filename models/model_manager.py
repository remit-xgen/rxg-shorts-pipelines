"""
Model Manager
Loads and manages AI models used in the pipeline
"""

import whisper
from ultralytics import YOLO
from logging.logger import logger
import config


class ModelManager:

    def __init__(self):

        self.whisper_model = None
        self.yolo_model = None

    # ==========================
    # WHISPER MODEL
    # ==========================

    def load_whisper(self):

        if self.whisper_model is None:

            logger.info(f"Loading Whisper model: {config.WHISPER_MODEL}")

            self.whisper_model = whisper.load_model(config.WHISPER_MODEL)

        return self.whisper_model

    # ==========================
    # YOLO MODEL
    # ==========================

    def load_yolo(self):

        if self.yolo_model is None:

            logger.info(f"Loading YOLO model: {config.YOLO_MODEL}")

            self.yolo_model = YOLO(config.YOLO_MODEL)

        return self.yolo_model


# global model manager
model_manager = ModelManager()
