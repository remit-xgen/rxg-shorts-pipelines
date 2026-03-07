"""
Speech Hook Detection
Find viral hook phrases in transcript
"""

from logging.logger import logger
from hook_detection.data.speech_hook_phrases import HOOK_PHRASES


class SpeechHookDetector:

    def __init__(self):

        self.hook_phrases = HOOK_PHRASES

    def detect(self, transcript):

        try:

            logger.info("Running speech hook detection")

            hooks = []

            for segment in transcript:

                text = segment["text"].lower()

                for phrase in self.hook_phrases:

                    if phrase in text:

                        hooks.append({
                            "time": segment["start"],
                            "text": segment["text"],
                            "phrase": phrase
                        })

            logger.info(f"Hooks detected: {len(hooks)}")

            return hooks

        except Exception as e:

            logger.error(f"Speech hook detection failed: {e}")
            return []
