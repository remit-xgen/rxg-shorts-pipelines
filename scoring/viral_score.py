
"""
Viral Score Calculator
Compute viral potential score for video moments
"""

from logging.logger import logger


class ViralScoreCalculator:

    def __init__(self):

        self.weights = {
            "speech_hook": 0.35,
            "visual_hook": 0.25,
            "emotion": 0.20,
            "audio": 0.10,
            "scene": 0.10
        }

    def calculate(
        self,
        time,
        speech_hooks,
        visual_hooks,
        emotions,
        audio_spikes,
        scenes
    ):

        score = 0

        if any(abs(h["time"] - time) < 1 for h in speech_hooks):
            score += self.weights["speech_hook"]

        if any(abs(h["time"] - time) < 1 for h in visual_hooks):
            score += self.weights["visual_hook"]

        if any(abs(e["time"] - time) < 1 for e in emotions):
            score += self.weights["emotion"]

        if any(abs(a["time"] - time) < 1 for a in audio_spikes):
            score += self.weights["audio"]

        if any(abs(s["start"] - time) < 1 for s in scenes):
            score += self.weights["scene"]

        return round(score, 3)
