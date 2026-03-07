"""
Cache Manager
Handles caching of pipeline data to avoid recomputation
"""

import os
import json
import hashlib

from logging.logger import logger


class CacheManager:

    def __init__(self, cache_dir="cache_store"):

        self.cache_dir = cache_dir

        os.makedirs(self.cache_dir, exist_ok=True)


    def _generate_key(self, name, params=None):

        """
        Create a unique cache key based on name and parameters
        """

        key_string = name

        if params:
            key_string += json.dumps(params, sort_keys=True)

        return hashlib.md5(key_string.encode()).hexdigest()


    def _cache_path(self, key):

        return os.path.join(self.cache_dir, f"{key}.json")


    def exists(self, name, params=None):

        key = self._generate_key(name, params)

        path = self._cache_path(key)

        return os.path.exists(path)


    def load(self, name, params=None):

        """
        Load cached data
        """

        key = self._generate_key(name, params)

        path = self._cache_path(key)

        if not os.path.exists(path):

            logger.info(f"Cache miss: {name}")

            return None

        try:

            with open(path, "r", encoding="utf-8") as f:

                data = json.load(f)

            logger.info(f"Cache loaded: {name}")

            return data

        except Exception as e:

            logger.error(f"Failed loading cache {name}: {e}")

            return None


    def save(self, name, data, params=None):

        """
        Save data to cache
        """

        key = self._generate_key(name, params)

        path = self._cache_path(key)

        try:

            with open(path, "w", encoding="utf-8") as f:

                json.dump(data, f, indent=2)

            logger.info(f"Cache saved: {name}")

        except Exception as e:

            logger.error(f"Failed saving cache {name}: {e}")


    def delete(self, name, params=None):

        key = self._generate_key(name, params)

        path = self._cache_path(key)

        if os.path.exists(path):

            os.remove(path)

            logger.info(f"Cache deleted: {name}")


    def clear(self):

        """
        Clear entire cache directory
        """

        try:

            for file in os.listdir(self.cache_dir):

                file_path = os.path.join(self.cache_dir, file)

                if os.path.isfile(file_path):

                    os.remove(file_path)

            logger.info("Cache cleared")

        except Exception as e:

            logger.error(f"Failed clearing cache: {e}")
