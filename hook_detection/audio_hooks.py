"""
Audio Hooks Detection
Detects potential hook moments based on audio energy spikes
"""

import numpy as np
import librosa

from logging.logger import logger


class AudioHooks:

    def __init__(self, energy_threshold=1.5):

        self.energy_threshold = energy_threshold


    def detect(self, audio_path):

        """
        Detect audio hook moments
        """

        try:

            logger.info("Detecting audio hooks")

            y, sr = librosa.load(audio_path, sr=None)

            # Compute short-time energy
            energy = np.array([
                sum(abs(y[i:i+1024]**2))
                for i in range(0, len(y), 1024)
            ])

            mean_energy = np.mean(energy)

            hooks = []

            for i, e in enumerate(energy):

                if e > mean_energy * self.energy_threshold:

                    timestamp = (i * 1024) / sr

                    hooks.append({
                        "type": "audio",
                        "time": timestamp,
                        "score": float(e / mean_energy)
                    })

            logger.info(f"Detected {len(hooks)} audio hooks")

            return hooks

        except Exception as e:

            logger.error(f"Audio hook detection failed: {e}")

            return []