"""
Central logging system for RXG Shorts AI Factory
"""

import logging
import os
from datetime import datetime


LOG_FOLDER = "logs"
os.makedirs(LOG_FOLDER, exist_ok=True)


def setup_logger(name="rxg_pipeline"):

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if logger.handlers:
        return logger

    # log filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(LOG_FOLDER, f"pipeline_{timestamp}.log")

    # file handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# global logger instance
logger = setup_logger()
