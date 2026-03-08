11"""
Frame Extractor
Extract frames from video based on timestamps
Optimized version
"""

import cv2
import os
import subprocess
from logging.logger import logger


class FrameExtractor:

    def __init__(self):
        pass


    def extract_frame(self, video_path, timestamp):

        """
        Extract a single frame at a specific timestamp (seconds)
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
        Extract multiple frames from a list of timestamps
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

                else:
                    logger.warning(f"Frame not found at {timestamp}s")

            cap.release()

            return frames

        except Exception as e:

            logger.error(f"Multiple frame extraction failed: {e}")
            return frames


    def extract_frames_ffmpeg(self, video_path, output_folder="frames", fps=1):

        """
        Fast frame extraction using FFmpeg
        Extract frames at given FPS (default 1 frame per second)
        """

        try:

            os.makedirs(output_folder, exist_ok=True)

            output_pattern = os.path.join(output_folder, "frame_%04d.jpg")

            command = [
                "ffmpeg",
                "-y",
                "-i", video_path,
                "-vf", f"fps={fps}",
                "-q:v", "2",
                output_pattern
            ]

            subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )

            logger.info(f"Frames extracted to {output_folder}")

            return output_folder

        except Exception as e:

            logger.error(f"FFmpeg frame extraction failed: {e}")
            return None