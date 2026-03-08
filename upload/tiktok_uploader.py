"""
TikTok Uploader
Stable automation using Playwright
Persistent login session
"""

import os
import time

from logging.logger import logger
from playwright.sync_api import sync_playwright


class TikTokUploader:

    def __init__(
        self,
        headless=False,
        user_data_dir="tiktok_session"
    ):

        self.headless = headless
        self.user_data_dir = user_data_dir

        os.makedirs(self.user_data_dir, exist_ok=True)


    def upload_video(
        self,
        video_path,
        caption
    ):

        try:

            logger.info("Starting TikTok upload")

            with sync_playwright() as p:

                browser = p.chromium.launch_persistent_context(

                    user_data_dir=self.user_data_dir,
                    headless=self.headless,
                    viewport={"width":1280,"height":900}

                )

                page = browser.new_page()

                page.goto("https://www.tiktok.com/upload")

                logger.info("Waiting for upload page")

                page.wait_for_timeout(5000)

                # ====================
                # Upload Video
                # ====================

                logger.info("Uploading video")

                file_input = page.locator("input[type='file']")

                file_input.set_input_files(video_path)

                # Wait for processing
                logger.info("Waiting for video processing")

                time.sleep(15)

                # ====================
                # Add Caption
                # ====================

                logger.info("Adding caption")

                caption_box = page.locator("div[contenteditable='true']").first

                caption_box.click()

                caption_box.fill(caption)

                time.sleep(3)

                # ====================
                # Post Video
                # ====================

                logger.info("Posting video")

                post_button = page.locator("button:has-text('Post')")

                post_button.click()

                time.sleep(10)

                logger.info("TikTok upload completed")

                browser.close()

                return True

        except Exception as e:

            logger.error(f"TikTok upload failed: {e}")

            return False