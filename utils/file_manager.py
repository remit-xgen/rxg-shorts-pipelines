"""
File Manager Utility
Handles folder creation, file paths, and cleanup
"""

import os
import shutil
from logging.logger import logger


class FileManager:

    @staticmethod
    def ensure_dir(path):
        """
        Create folder if it doesn't exist
        """
        if not os.path.exists(path):
            os.makedirs(path)
            logger.info(f"Created directory: {path}")

    @staticmethod
    def file_exists(path):
        """
        Check if file exists
        """
        return os.path.isfile(path)

    @staticmethod
    def delete_file(path):
        """
        Delete file safely
        """
        if os.path.exists(path):
            os.remove(path)
            logger.info(f"Deleted file: {path}")

    @staticmethod
    def delete_folder(path):
        """
        Delete folder safely
        """
        if os.path.exists(path):
            shutil.rmtree(path)
            logger.info(f"Deleted folder: {path}")

    @staticmethod
    def list_files(folder):
        """
        List all files in folder
        """
        if not os.path.exists(folder):
            return []

        return [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if os.path.isfile(os.path.join(folder, f))
        ]

    @staticmethod
    def move_file(src, dst):
        """
        Move file
        """
        shutil.move(src, dst)
        logger.info(f"Moved file {src} -> {dst}")

    @staticmethod
    def cleanup_temp_folders():

        folders = [
            "downloads",
            "temp",
            "frames",
            "audio",
            "clips"
        ]

        for folder in folders:

            if os.path.exists(folder):

                try:
                    shutil.rmtree(folder)
                    os.makedirs(folder)

                    logger.info(f"Cleaned folder: {folder}")

                except Exception as e:
                    logger.error(f"Cleanup failed for {folder}: {e}")
