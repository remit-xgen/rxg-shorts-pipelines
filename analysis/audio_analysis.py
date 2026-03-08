"""
Audio Analysis
Detect high-energy moments in audio
Optimized for Colab Free
"""

import librosa
import numpy as np

from logging.logger import logger


class AudioAnalyzer:

    def __init__(
        self,
        energy_threshold=1.5,
        hop_length=512
    ):

        self.energy_threshold = energy_threshold
        self.hop_length = hop_length


    def analyze(self, audio_path):

        """
        Returns list of high energy moments

        [
            {
                "time": float,
                "energy": float
            }
        ]
        """

        try:

            logger.info(f"Analyzing audio: {audio_path}")

            y, sr = librosa.load(
                audio_path,
                sr=None,
                mono=True
            )

            # RMS energy
            energy = librosa.feature.rms(
                y=y,
                hop_length=self.hop_length
            )[0]

            avg_energy = float(np.mean(energy))

            moments = []

            for i, e in enumerate(energy):

                if e > avg_energy * self.energy_threshold:

                    time_sec = librosa.frames_to_time(
                        i,
                        sr=sr,
                        hop_length=self.hop_length
                    )

                    moments.append({
                        "time": float(time_sec),
                        "energy": float(e)
                    })

            logger.info(
                f"High energy moments detected: {len(moments)}"
            )

            return moments

        except Exception as e:

            logger.error(f"Audio analysis failed: {e}")

            return []