import random
import re

from logging.logger import logger
from metadata.data.caption_templates import CAPTION_TEMPLATES


class CaptionGenerator:

    def __init__(self):

        self.max_caption_length = 120

        self.viral_emojis = [
            "🔥", "🤯", "😳", "💡", "🚀", "⚡"
        ]

        self.default_hashtags = [
            "#shorts",
            "#viral",
            "#fyp"
        ]

    def generate(self, transcript, topic=None):

        try:

            logger.info("Generating caption")

            topic = topic or self._extract_topic(transcript)

            template = random.choice(CAPTION_TEMPLATES)

            caption = template.format(topic=topic)

            caption = self._inject_emoji(caption)

            hashtags = self._generate_hashtags(topic)

            final_caption = f"{caption}\n\n{hashtags}"

            return final_caption[: self.max_caption_length]

        except Exception as e:

            logger.error(f"Caption generation failed: {e}")
            return "Watch this 🔥"

    def _extract_topic(self, transcript):

        if not transcript:
            return "this"

        text = " ".join(
            seg["text"] for seg in transcript[:3]
        ).lower()

        words = re.findall(r"\b[a-z]{4,}\b", text)

        if not words:
            return "this"

        return random.choice(words)

    def _inject_emoji(self, caption):

        emoji = random.choice(self.viral_emojis)

        return f"{caption} {emoji}"

    def _generate_hashtags(self, topic):

        topic_tag = f"#{topic.replace(' ', '')}"

        tags = [topic_tag] + self.default_hashtags

        return " ".join(tags)