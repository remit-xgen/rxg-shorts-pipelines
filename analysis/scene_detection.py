"""
Scene Detection
Detect scene changes in video
Optimized for Colab Free
"""

from scenedetect import VideoManager, SceneManager
from scenedetect.detectors import ContentDetector

from logging.logger import logger


class SceneDetector:

    def __init__(
        self,
        threshold=30.0,
        downscale_factor=2
    ):

        self.threshold = threshold
        self.downscale_factor = downscale_factor


    def detect(self, video_path):

        """
        Returns scenes:

        [
            {
                "start": float,
                "end": float
            }
        ]
        """

        try:

            logger.info(f"Running scene detection: {video_path}")

            video_manager = VideoManager([video_path])

            # reduce CPU usage
            if self.downscale_factor > 1:
                video_manager.set_downscale_factor(
                    self.downscale_factor
                )

            scene_manager = SceneManager()

            scene_manager.add_detector(
                ContentDetector(
                    threshold=self.threshold
                )
            )

            video_manager.start()

            scene_manager.detect_scenes(
                frame_source=video_manager
            )

            scene_list = scene_manager.get_scene_list()

            scenes = []

            for scene in scene_list:

                start = scene[0].get_seconds()
                end = scene[1].get_seconds()

                scenes.append({
                    "start": float(start),
                    "end": float(end)
                })

            logger.info(
                f"Scenes detected: {len(scenes)}"
            )

            video_manager.release()

            return scenes

        except Exception as e:

            logger.error(
                f"Scene detection failed: {e}"
            )

            return []