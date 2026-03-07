"""
Face Detection
Detect human faces in video frames
"""

import cv2
from logging.logger import logger


class FaceDetector:

    def __init__(self):

        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            "haarcascade_frontalface_default.xml"
        )

    def detect(self, video_path, sample_rate=10):

        try:

            logger.info(f"Running face detection: {video_path}")

            cap = cv2.VideoCapture(video_path)

            fps = cap.get(cv2.CAP_PROP_FPS)

            frame_interval = int(fps * sample_rate)

            frame_index = 0

            faces_data = []

            while True:

                ret, frame = cap.read()

                if not ret:
                    break

                if frame_index % frame_interval == 0:

                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    faces = self.face_cascade.detectMultiScale(
                        gray,
                        scaleFactor=1.3,
                        minNeighbors=5
                    )

                    time_sec = frame_index / fps

                    faces_data.append({
                        "time": time_sec,
                        "faces": len(faces)
                    })

                frame_index += 1

            cap.release()

            logger.info(f"Face samples collected: {len(faces_data)}")

            return faces_data

        except Exception as e:

            logger.error(f"Face detection failed: {e}")
            return []
