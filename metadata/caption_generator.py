import random

from logging.logger import logger
from metadata.data.caption_templates import CAPTION_TEMPLATES


class CaptionGenerator:

    def generate(self, transcript, topic="this"):

        try:

            logger.info("Generating caption")

            template = random.choice(CAPTION_TEMPLATES)

            caption = template.format(topic=topic)

            return caption

        except Exception as e:

            logger.error(f"Caption generation failed: {e}")
            return "Watch this!"
