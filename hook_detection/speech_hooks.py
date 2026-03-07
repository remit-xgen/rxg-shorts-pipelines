"""
Speech Hook Detection
Find viral hook phrases in transcript
"""

from logging.logger import logger


class SpeechHookDetector:

    def __init__(self):

        self.hook_phrases = [
            "you won't believe",
            "wait for it",
            "this changed everything",
            "nobody talks about",
            "here's the secret",
            "watch this",
            "this is crazy",
            "i discovered",
            "this is why",
            "what happened next",
            "this will shock you",
            "the truth is"
        ]

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
