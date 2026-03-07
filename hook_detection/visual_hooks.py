"""
Visual Hook Detection
Combine visual signals to detect hook moments
"""

from logging.logger import logger


class VisualHookDetector:

    def __init__(self):

        self.motion_weight = 0.4
        self.face_weight = 0.2
        self.emotion_weight = 0.3
        self.audio_weight = 0.1

    def detect(self, gestures, faces, emotions, audio_spikes):

        try:

            logger.info("Running visual hook detection")

            hooks = []

            candidate_times = set()

            for g in gestures:
                candidate_times.add(round(g["time"]))

            for f in faces:
                candidate_times.add(round(f["time"]))

            for e in emotions:
                candidate_times.add(round(e["time"]))

            for a in audio_spikes:
                candidate_times.add(round(a["time"]))

            for t in sorted(candidate_times):

                score = 0

                motion = any(abs(g["time"] - t) < 1 for g in gestures)
                face = any(abs(f["time"] - t) < 1 for f in faces)
                emotion = any(abs(e["time"] - t) < 1 for e in emotions)
                audio = any(abs(a["time"] - t) < 1 for a in audio_spikes)

                if motion:
                    score += self.motion_weight

                if face:
                    score += self.face_weight

                if emotion:
                    score += self.emotion_weight

                if audio:
                    score += self.audio_weight

                if score > 0.5:

                    hooks.append({
                        "time": t,
                        "score": round(score, 2)
                    })

            logger.info(f"Visual hooks detected: {len(hooks)}")

            return hooks

        except Exception as e:

            logger.error(f"Visual hook detection failed: {e}")
            return []
