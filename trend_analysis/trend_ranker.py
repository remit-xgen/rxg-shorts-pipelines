"""
Trend Ranker
Ranks trending keywords based on simple scoring
"""

from logging.logger import logger


class TrendRanker:

    def __init__(self):

        pass


    def rank(self, keywords):

        """
        Rank keywords based on position and heuristics
        """

        try:

            logger.info("Ranking trending keywords")

            ranked = []

            total = len(keywords)

            for i, keyword in enumerate(keywords):

                # basic score (higher if higher position)
                position_score = (total - i) / total

                # keyword specificity bonus
                word_count = len(keyword.split())
                specificity_bonus = word_count * 0.05

                score = position_score + specificity_bonus

                ranked.append({
                    "keyword": keyword,
                    "score": score
                })

            ranked = sorted(
                ranked,
                key=lambda x: x["score"],
                reverse=True
            )

            logger.info(f"Ranked {len(ranked)} keywords")

            return ranked

        except Exception as e:

            logger.error(f"Trend ranking failed: {e}")

            return []