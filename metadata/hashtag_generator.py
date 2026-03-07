"""
Hashtag Generator
Generates hashtags based on topic
"""

import random

from logging.logger import logger
from metadata.data.hashtag_data import BASE_HASHTAGS, NICHE_HASHTAGS


class HashtagGenerator:

    def generate(self, niche="general"):

        try:

            logger.info("Generating hashtags")

            hashtags = []

            hashtags.extend(BASE_HASHTAGS)

            if niche in NICHE_HASHTAGS:

                niche_tags = random.sample(
                    NICHE_HASHTAGS[niche],
                    min(3, len(NICHE_HASHTAGS[niche]))
                )

                hashtags.extend(niche_tags)

            hashtags = [f"#{tag}" for tag in hashtags]

            return " ".join(hashtags)

        except Exception as e:

            logger.error(f"Hashtag generation failed: {e}")
            return "#shorts #viral"
