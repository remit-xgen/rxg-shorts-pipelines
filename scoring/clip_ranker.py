"""
Clip Ranker
Rank candidate clips based on viral score
"""

from logging.logger import logger
from scoring.viral_score import ViralScoreCalculator


class ClipRanker:

    def __init__(self):

        self.score_calculator = ViralScoreCalculator()

        self.clip_min_length = 8
        self.clip_max_length = 35

    def rank(
        self,
        duration,
        speech_hooks,
        visual_hooks,
        emotions,
        audio_spikes,
        scenes
    ):

        try:

            logger.info("Ranking candidate clips")

            candidate_times = set()

            for h in speech_hooks:
                candidate_times.add(round(h["time"]))

            for h in visual_hooks:
                candidate_times.add(round(h["time"]))

            for e in emotions:
                candidate_times.add(round(e["time"]))

            for a in audio_spikes:
                candidate_times.add(round(a["time"]))

            ranked_clips = []

            for t in sorted(candidate_times):

                score = self.score_calculator.calculate(
                    t,
                    speech_hooks,
                    visual_hooks,
                    emotions,
                    audio_spikes,
                    scenes
                )

                if score < 0.35:
                    continue

                start = max(0, t - 3)
                end = min(duration, t + 12)

                clip_length = end - start

                if clip_length < self.clip_min_length:
                    end = start + self.clip_min_length

                if clip_length > self.clip_max_length:
                    end = start + self.clip_max_length

                ranked_clips.append({
                    "start": round(start, 2),
                    "end": round(end, 2),
                    "score": score
                })

            ranked_clips.sort(key=lambda x: x["score"], reverse=True)

            logger.info(f"Clips ranked: {len(ranked_clips)}")

            return ranked_clips

        except Exception as e:

            logger.error(f"Clip ranking failed: {e}")
            return []
