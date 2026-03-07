"""
Keyword Expander
Expands a base keyword into multiple search variations
"""

from logging.logger import logger


class KeywordExpander:

    def __init__(self):

        self.prefixes = [
            "best",
            "top",
            "viral",
            "trending"
        ]

        self.suffixes = [
            "tutorial",
            "tips",
            "explained",
            "2025",
            "for beginners"
        ]


    def expand(self, topic):

        """
        Expand a topic into multiple keyword variations
        """

        try:

            logger.info(f"Expanding keywords for topic: {topic}")

            keywords = set()

            keywords.add(topic)

            for prefix in self.prefixes:

                keywords.add(f"{prefix} {topic}")

            for suffix in self.suffixes:

                keywords.add(f"{topic} {suffix}")

            expanded_keywords = list(keywords)

            logger.info(f"Generated {len(expanded_keywords)} keywords")

            return expanded_keywords

        except Exception as e:

            logger.error(f"Keyword expansion failed: {e}")

            return [topic]