"""
Thumbnail Generator
Extracts a frame from video to use as thumbnail
"""

import os
import uuid
import cv2

from logging.logger import logger


class ThumbnailGenerator:

    def __init__(self, output_dir="thumbnails"):

        self.output_dir = output_dir

        os.makedirs(self.output_dir, exist_ok=True)


    def generate(self, video_path):

        """
        Generate thumbnail from video
        """

        try:

            logger.info("Generating thumbnail")

            cap = cv2.VideoCapture(video_path)

            if not cap.isOpened():

                logger.error("Failed to open video")

                return None

            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            middle_frame = total_frames // 2

            cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame)

            success, frame = cap.read()

            cap.release()

            if not success:

                logger.error("Failed to read frame")

                return None

            thumbnail_path = os.path.join(
                self.output_dir,
                f"thumb_{uuid.uuid4().hex}.png"
            )

            cv2.imwrite(thumbnail_path, frame)

            logger.info(f"Thumbnail saved: {thumbnail_path}")

            return thumbnail_path

        except Exception as e:

            logger.error(f"Thumbnail generation failed: {e}")

            return None