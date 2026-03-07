"""
Global configuration for RXG Shorts AI Factory
Optimized for Google Colab Free
"""

import os

# ==============================
# GENERAL PIPELINE SETTINGS
# ==============================

MAX_VIDEOS = 5
SHORTS_PER_VIDEO = 3
MAX_SHORTS_EXPORT = 10

BATCH_SIZE = 2

# ==============================
# PATH SETTINGS
# ==============================

BASE_DIR = os.getcwd()

DOWNLOAD_DIR = os.path.join(BASE_DIR, "downloads")
CACHE_DIR = os.path.join(BASE_DIR, "cache_store")
OUTPUT_DIR = os.path.join(BASE_DIR, "exports")
TEMP_DIR = os.path.join(BASE_DIR, "temp")

# create folders if missing
for folder in [DOWNLOAD_DIR, CACHE_DIR, OUTPUT_DIR, TEMP_DIR]:
    os.makedirs(folder, exist_ok=True)

# ==============================
# VIDEO SETTINGS
# ==============================

TARGET_ASPECT_RATIO = "9:16"

MAX_CLIP_LENGTH = 45
MIN_CLIP_LENGTH = 10

FPS_SAMPLE_RATE = 2

# ==============================
# AI MODEL SETTINGS
# ==============================

WHISPER_MODEL = "base"

YOLO_MODEL = "yolov8n.pt"

ENABLE_EMOTION_DETECTION = True
ENABLE_GESTURE_DETECTION = True

# ==============================
# TREND DISCOVERY
# ==============================

MAX_TRENDS = 5
KEYWORDS_PER_TREND = 5

# ==============================
# EXPORT SETTINGS
# ==============================

EXPORT_RESOLUTION = (1080, 1920)
EXPORT_FPS = 30

VIDEO_CODEC = "libx264"
AUDIO_CODEC = "aac"

# ==============================
# PARALLEL PROCESSING
# ==============================

MAX_WORKERS = 2

# ==============================
# DEBUG
# ==============================

DEBUG_MODE = True
