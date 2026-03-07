"""
TikTok Uploader
Uploads shorts to TikTok using Playwright automation
"""

import time

from logging.logger import logger

from playwright.sync_api import sync_playwright


class TikTokUploader:

    def __init__(self, headless=False):

        self.headless = headless


    def upload_video(
        self,
        video_path,
        caption
    ):

        try:

            logger.info("Starting TikTok upload")

            with sync_playwright() as p:

                browser = p.chromium.launch(
                    headless=self.headless
                )

                context = browser.new_context()

                page = context.new_page()

                page.goto("https://www.tiktok.com/upload")

                logger.info("Waiting for login if needed...")

                time.sleep(30)

                file_input = page.locator("input[type='file']")

                file_input.set_input_files(video_path)

                logger.info("Uploading video file")

                time.sleep(10)

                caption_box = page.locator(
                    "[contenteditable='true']"
                )

                caption_box.click()

                caption_box.fill(caption)

                logger.info("Caption added")

                time.sleep(5)

                post_button = page.get_by_text("Post")

                post_button.click()

                logger.info("Video posted to TikTok")

                time.sleep(10)

                browser.close()

                return True

        except Exception as e:

            logger.error(f"TikTok upload failed: {e}")

            return False
