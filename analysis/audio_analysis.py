"""
Audio Analysis
Detect high-energy moments in audio
"""

import librosa
import numpy as np
from logging.logger import logger


class AudioAnalyzer:

    def __init__(self, energy_threshold=1.5):
        self.energy_threshold = energy_threshold

    def analyze(self, audio_path):

        try:

            logger.info(f"Analyzing audio: {audio_path}")

            y, sr = librosa.load(audio_path)

            energy = librosa.feature.rms(y=y)[0]

            avg_energy = np.mean(energy)

            moments = []

            for i, e in enumerate(energy):

                if e > avg_energy * self.energy_threshold:

                    time_sec = librosa.frames_to_time(i, sr=sr)

                    moments.append({
                        "time": float(time_sec),
                        "energy": float(e)
                    })

            logger.info(f"High energy moments: {len(moments)}")

            return moments

        except Exception as e:

            logger.error(f"Audio analysis failed: {e}")
            return []
