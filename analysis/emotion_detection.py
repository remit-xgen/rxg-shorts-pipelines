"""
Emotion Detection
Detect facial emotions in video frames
"""

import cv2
from deepface import DeepFace
from logging.logger import logger


class EmotionDetector:

    def __init__(self):
        pass

    def detect(self, video_path, sample_rate=5):

        try:

            logger.info(f"Running emotion detection: {video_path}")

            cap = cv2.VideoCapture(video_path)

            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_interval = int(fps * sample_rate)

            frame_index = 0

            emotions = []

            while True:

                ret, frame = cap.read()

                if not ret:
                    break

                if frame_index % frame_interval == 0:

                    try:

                        result = DeepFace.analyze(
                            frame,
                            actions=['emotion'],
                            enforce_detection=False
                        )

                        emotion = result[0]['dominant_emotion']

                        time_sec = frame_index / fps

                        emotions.append({
                            "time": time_sec,
                            "emotion": emotion
                        })

                    except:
                        pass

                frame_index += 1

            cap.release()

            logger.info(f"Emotion samples: {len(emotions)}")

            return emotions

        except Exception as e:

            logger.error(f"Emotion detection failed: {e}")
            return []
