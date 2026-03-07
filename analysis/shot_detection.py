"""
Shot Detection
Detect fine-grained shot boundaries
"""

import cv2
from logging.logger import logger


class ShotDetector:

    def __init__(self, threshold=30):
        self.threshold = threshold

    def detect(self, video_path):

        try:

            logger.info(f"Running shot detection: {video_path}")

            cap = cv2.VideoCapture(video_path)

            shots = []
            prev_hist = None
            frame_index = 0
            fps = cap.get(cv2.CAP_PROP_FPS)

            while True:

                ret, frame = cap.read()

                if not ret:
                    break

                hist = cv2.calcHist(
                    [frame],
                    [0],
                    None,
                    [256],
                    [0, 256]
                )

                if prev_hist is not None:

                    diff = cv2.compareHist(
                        prev_hist,
                        hist,
                        cv2.HISTCMP_BHATTACHARYYA
                    )

                    if diff > self.threshold / 100:

                        time_sec = frame_index / fps

                        shots.append({
                            "time": time_sec
                        })

                prev_hist = hist
                frame_index += 1

            cap.release()

            logger.info(f"Shots detected: {len(shots)}")

            return shots

        except Exception as e:

            logger.error(f"Shot detection failed: {e}")
            return []
