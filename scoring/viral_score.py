"""
Advanced Viral Score Engine
Multi-signal viral potential scoring
Designed for high-precision short-form extraction
"""

import numpy as np
from logging.logger import logger


class ViralScoreCalculator:

    def __init__(self):

        self.weights = {
            "speech_hook": 0.30,
            "visual_hook": 0.20,
            "emotion": 0.20,
            "audio": 0.15,
            "scene": 0.15
        }

        self.window = 2.0

    def _within_window(self, t1, t2):
        return abs(t1 - t2) <= self.window

    def _density_score(self, time, events):

        count = 0

        for e in events:
            if self._within_window(time, e["time"]):
                count += 1

        return min(count / 3, 1)

    def _emotion_intensity(self, time, emotions):

        values = []

        for e in emotions:

            if self._within_window(time, e["time"]):
                values.append(e.get("score", 0.5))

        if not values:
            return 0

        return np.mean(values)

    def _audio_spike_intensity(self, time, spikes):

        values = []

        for a in spikes:

            if self._within_window(time, a["time"]):
                values.append(a.get("strength", 0.5))

        if not values:
            return 0

        return np.mean(values)

    def _scene_change_score(self, time, scenes):

        for s in scenes:

            if self._within_window(time, s["start"]):
                return 1

        return 0

    def calculate(
        self,
        time,
        speech_hooks,
        visual_hooks,
        emotions,
        audio_spikes,
        scenes
    ):

        speech_density = self._density_score(time, speech_hooks)
        visual_density = self._density_score(time, visual_hooks)

        emotion_strength = self._emotion_intensity(time, emotions)
        audio_strength = self._audio_spike_intensity(time, audio_spikes)

        scene_change = self._scene_change_score(time, scenes)

        score = (
            speech_density * self.weights["speech_hook"] +
            visual_density * self.weights["visual_hook"] +
            emotion_strength * self.weights["emotion"] +
            audio_strength * self.weights["audio"] +
            scene_change * self.weights["scene"]
        )

        return round(score * 100, 2)

    def rank_moments(
        self,
        candidate_times,
        speech_hooks,
        visual_hooks,
        emotions,
        audio_spikes,
        scenes
    ):

        scored = []

        for t in candidate_times:

            score = self.calculate(
                t,
                speech_hooks,
                visual_hooks,
                emotions,
                audio_spikes,
                scenes
            )

            scored.append({
                "time": t,
                "score": score
            })

        scored.sort(key=lambda x: x["score"], reverse=True)

        logger.info(f"Top viral moment score: {scored[0]['score'] if scored else 0}")

        return scored

    def top_moments(
        self,
        candidate_times,
        speech_hooks,
        visual_hooks,
        emotions,
        audio_spikes,
        scenes,
        top_k=10
    ):

        ranked = self.rank_moments(
            candidate_times,
            speech_hooks,
            visual_hooks,
            emotions,
            audio_spikes,
            scenes
        )

        return ranked[:top_k]