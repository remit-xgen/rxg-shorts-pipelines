import ffmpeg
from rxg_logging.logger import logger

class NormalizeVideo:

    def __init__(self, target_fps=30, resolution="1080x1920"):
        self.target_fps = target_fps
        self.resolution = resolution

    def process(self, input_path, output_path):
        try:
            (
                ffmpeg
                .input(input_path)
                .filter("scale", 1080, 1920)
                .filter("fps", fps=self.target_fps)
                .output(output_path)
                .overwrite_output()
                .run()
            )

            logger.info(f"Video normalized: {output_path}")

        except Exception as e:
            logger.error(f"NormalizeVideo error: {e}")
            raise
