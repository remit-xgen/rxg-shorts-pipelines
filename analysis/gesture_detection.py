"""
Gesture Detection
Detect motion intensity in video frames
"""

import cv2
import numpy as np
from logging.logger import logger


class GestureDetector:

    def __init__(self, motion_threshold=25):
        self.motion_threshold = motion_threshold

    def detect(self, video_path):

        try:

            logger.info(f"Running gesture detection: {video_path}")

            cap = cv2.VideoCapture(video_path)

            ret, prev_frame = cap.read()

            if not ret:
                return []

            prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

            frame_index = 1
            fps = cap.get(cv2.CAP_PROP_FPS)

            gestures = []

            while True:

                ret, frame = cap.read()

                if not ret:
                    break

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                frame_diff = cv2.absdiff(prev_gray, gray)

                motion_score = np.mean(frame_diff)

                if motion_score > self.motion_threshold:

                    time_sec = frame_index / fps

                    gestures.append({
                        "time": time_sec,
                        "motion": float(motion_score)
                    })

                prev_gray = gray
                frame_index += 1

            cap.release()

            logger.info(f"Gesture moments detected: {len(gestures)}")

            return gestures

        except Exception as e:

            logger.error(f"Gesture detection failed: {e}")
            return []
