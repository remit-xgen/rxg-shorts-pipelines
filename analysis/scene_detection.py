"""
Scene Detection
Detect scene changes in video
"""

from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector
from logging.logger import logger


class SceneDetector:

    def __init__(self, threshold=30.0):
        self.threshold = threshold

    def detect(self, video_path):

        try:

            logger.info(f"Running scene detection: {video_path}")

            video_manager = VideoManager([video_path])
            scene_manager = SceneManager()

            scene_manager.add_detector(
                ContentDetector(threshold=self.threshold)
            )

            video_manager.start()

            scene_manager.detect_scenes(frame_source=video_manager)

            scene_list = scene_manager.get_scene_list()

            scenes = []

            for scene in scene_list:

                start = scene[0].get_seconds()
                end = scene[1].get_seconds()

                scenes.append({
                    "start": start,
                    "end": end
                })

            logger.info(f"Scenes detected: {len(scenes)}")

            return scenes

        except Exception as e:

            logger.error(f"Scene detection failed: {e}")
            return []
