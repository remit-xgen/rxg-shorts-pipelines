"""
FPS Sampler
Samples frames from video at a lower FPS for faster processing
"""

import cv2
from logging.logger import logger


class FPSSampler:

    def __init__(self, sample_fps=2):
        """
        sample_fps: number of frames per second to sample
        """
        self.sample_fps = sample_fps


    def sample(self, video_path):

        """
        Generator that yields sampled frames
        """

        try:

            cap = cv2.VideoCapture(video_path)

            if not cap.isOpened():
                logger.error(f"Failed to open video: {video_path}")
                return

            original_fps = cap.get(cv2.CAP_PROP_FPS)

            if original_fps == 0:
                original_fps = 30

            frame_interval = int(original_fps / self.sample_fps)

            frame_index = 0

            logger.info(
                f"Sampling video at {self.sample_fps} FPS (original: {original_fps})"
            )

            while True:

                ret, frame = cap.read()

                if not ret:
                    break

                if frame_index % frame_interval == 0:

                    timestamp = frame_index / original_fps

                    yield {
                        "frame": frame,
                        "timestamp": timestamp,
                        "frame_index": frame_index
                    }

                frame_index += 1

            cap.release()

        except Exception as e:

            logger.error(f"FPS sampling failed: {e}")