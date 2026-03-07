"""
Portrait Crop
Convert landscape clips to portrait 9:16
"""

import cv2
import os
import subprocess

from logging.logger import logger


class PortraitCrop:

    def __init__(self):

        self.output_dir = "workspace/portrait_clips"
        os.makedirs(self.output_dir, exist_ok=True)

        self.face_detector = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    def detect_face_center(self, video_path):

        cap = cv2.VideoCapture(video_path)

        ret, frame = cap.read()

        if not ret:
            return None

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = self.face_detector.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5
        )

        cap.release()

        if len(faces) == 0:
            return None

        x, y, w, h = faces[0]

        center_x = x + w // 2

        return center_x

    def crop(self, clips):

        try:

            logger.info("Converting clips to portrait")

            portrait_clips = []

            for i, clip in enumerate(clips):

                video_path = clip["path"]

                cap = cv2.VideoCapture(video_path)

                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                cap.release()

                target_width = int(height * 9 / 16)

                center_x = self.detect_face_center(video_path)

                if center_x is None:
                    center_x = width // 2

                x1 = max(0, center_x - target_width // 2)

                if x1 + target_width > width:
                    x1 = width - target_width

                output_path = os.path.join(
                    self.output_dir,
                    f"portrait_{i}.mp4"
                )

                crop_filter = f"crop={target_width}:{height}:{x1}:0"

                command = [
                    "ffmpeg",
                    "-y",
                    "-i", video_path,
                    "-vf", crop_filter,
                    "-c:a", "copy",
                    output_path
                ]

                subprocess.run(
                    command,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )

                portrait_clips.append({
                    "path": output_path,
                    "cuts": clip["cuts"],
                    "score": clip["score"]
                })

            logger.info("Portrait crop completed")

            return portrait_clips

        except Exception as e:

            logger.error(f"Portrait crop failed: {e}")
            return []
