"""
Clip Ranking Engine
Score and rank potential viral clips
"""

from logging.logger import logger


class ClipRanker:

    def __init__(self):

        # weight configuration
        self.speech_weight = 0.35
        self.visual_weight = 0.30
        self.emotion_weight = 0.20
        self.audio_weight = 0.15

    def rank(self, speech_hooks, visual_hooks, emotions, audio_spikes):

        try:

            logger.info("Running clip ranking engine")

            candidates = []

            times = set()

            for h in speech_hooks:
                times.add(round(h["time"]))

            for h in visual_hooks:
                times.add(round(h["time"]))

            for e in emotions:
                times.add(round(e["time"]))

            for a in audio_spikes:
                times.add(round(a["time"]))

            for t in sorted(times):

                speech_score = 1 if any(abs(h["time"] - t) < 1 for h in speech_hooks) else 0

                visual_score = next((h["score"] for h in visual_hooks if abs(h["time"] - t) < 1), 0)

                emotion_score = 1 if any(abs(e["time"] - t) < 1 for e in emotions) else 0

                audio_score = 1 if any(abs(a["time"] - t) < 1 for a in audio_spikes) else 0

                score = (
                    speech_score * self.speech_weight +
                    visual_score * self.visual_weight +
                    emotion_score * self.emotion_weight +
                    audio_score * self.audio_weight
                )

                candidates.append({
                    "time": t,
                    "score": round(score, 3)
                })

            ranked = sorted(candidates, key=lambda x: x["score"], reverse=True)

            logger.info(f"Clips ranked: {len(ranked)}")

            return ranked

        except Exception as e:

            logger.error(f"Clip ranking failed: {e}")
            return []
