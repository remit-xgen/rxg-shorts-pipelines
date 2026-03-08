"""
Trend Ranker
Advanced Viral Intelligence Ranking Engine
"""

import random
from logging.logger import logger

from trend_analysis.data.viral_triggers import VIRAL_TRIGGERS
from trend_analysis.data.high_interest_topics import HIGH_INTEREST_TOPICS
from trend_analysis.data.curiosity_words import CURIOSITY_WORDS


class TrendRanker:

    def __init__(self):

        pass


    def rank(self, keywords):

        try:

            logger.info("Running viral intelligence ranking")

            ranked = []

            total = len(keywords)

            for i, keyword in enumerate(keywords):

                keyword_lower = keyword.lower()

                score = 0


                # =========================
                # Position Score
                # =========================

                position_score = (total - i) / total

                score += position_score * 2


                # =========================
                # Keyword Length Score
                # =========================

                word_count = len(keyword.split())

                if 2 <= word_count <= 5:

                    score += 1.5

                else:

                    score += 0.5


                # =========================
                # Viral Trigger Words
                # =========================

                for trigger in VIRAL_TRIGGERS:

                    if trigger in keyword_lower:

                        score += 2


                # =========================
                # High Interest Topic Boost
                # =========================

                for topic in HIGH_INTEREST_TOPICS:

                    if topic in keyword_lower:

                        score += 2.5


                # =========================
                # Curiosity Words
                # =========================

                for word in CURIOSITY_WORDS:

                    if word in keyword_lower:

                        score += 1.2


                # =========================
                # Exploration Factor
                # =========================

                score += random.uniform(0, 0.5)


                ranked.append({

                    "keyword": keyword,
                    "score": round(score, 4)

                })


            ranked = sorted(

                ranked,
                key=lambda x: x["score"],
                reverse=True

            )

            logger.info(f"Ranked {len(ranked)} trends")

            return ranked


        except Exception as e:

            logger.error(f"Trend ranking failed: {e}")

            return []