"""
Hook Generator
Combines speech, audio, and visual hooks into unified hook candidates
"""

from logging.logger import logger

from hook_detection.speech_hooks import SpeechHooks
from hook_detection.audio_hooks import AudioHooks
from hook_detection.visual_hooks import VisualHooks


class HookGenerator:

    def __init__(self):

        self.speech_detector = SpeechHooks()
        self.audio_detector = AudioHooks()
        self.visual_detector = VisualHooks()


    def generate(self, transcript, scenes, audio_path):

        """
        Generate hook candidates from multiple detectors
        """

        try:

            logger.info("Generating hooks")

            speech_hooks = self.speech_detector.detect(transcript)

            audio_hooks = self.audio_detector.detect(audio_path)

            visual_hooks = self.visual_detector.detect(scenes)

            hooks = []

            hooks.extend(speech_hooks)
            hooks.extend(audio_hooks)
            hooks.extend(visual_hooks)

            hooks = sorted(
                hooks,
                key=lambda x: x["time"]
            )

            logger.info(f"Total hooks generated: {len(hooks)}")

            return hooks

        except Exception as e:

            logger.error(f"Hook generation failed: {e}")

            return []