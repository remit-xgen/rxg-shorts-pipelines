"""
RXG AI Shorts Factory
Main Pipeline Entry Point
"""

from logging.logger import logger

from pipeline_orchestrator import PipelineOrchestrator


def main():

    try:

        logger.info("RXG AI Factory Starting")

        pipeline = PipelineOrchestrator()

        pipeline.run()

        logger.info("RXG AI Factory Finished")

    except Exception as e:

        logger.error(f"Pipeline crashed: {e}")


if __name__ == "__main__":

    main()
