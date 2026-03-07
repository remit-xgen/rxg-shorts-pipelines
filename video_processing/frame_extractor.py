"""
Frame Extractor
Extract frames from video based on timestamps
"""

import cv2
from logging.logger import logger


class FrameExtractor:

    def __init__(self):
        pass


    def extract_frame(self, video_path, timestamp):

        """
        Extract single frame at a specific timestamp
        """

        try:

            cap = cv2.VideoCapture(video_path)

            if not cap.isOpened():
                logger.error(f"Cannot open video: {video_path}")
                return None

            fps = cap.get(cv2.CAP_PROP_FPS)

            frame_number = int(timestamp * fps)

            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

            ret, frame = cap.read()

            cap.release()

            if not ret:
                logger.warning(f"Frame not found at {timestamp}s")
                return None

            return frame

        except Exception as e:

            logger.error(f"Frame extraction failed: {e}")
            return None


    def extract_multiple(self, video_path, timestamps):

        """
        Extract multiple frames from list of timestamps
        """

        frames = []

        try:

            cap = cv2.VideoCapture(video_path)

            if not cap.isOpened():
                logger.error(f"Cannot open video: {video_path}")
                return frames

            fps = cap.get(cv2.CAP_PROP_FPS)

            for timestamp in timestamps:

                frame_number = int(timestamp * fps)

                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

                ret, frame = cap.read()

                if ret:
                    frames.append({
                        "timestamp": timestamp,
                        "frame": frame
                    })

            cap.release()

            return frames

        except Exception as e:

            logger.error(f"Multiple frame extraction failed: {e}")
            return frames