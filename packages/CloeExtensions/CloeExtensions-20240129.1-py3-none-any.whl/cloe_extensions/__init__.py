import logging
import os

logger = logging.getLogger(__name__)
logger.propagate = False
handler = logging.StreamHandler()
if os.getenv("SYSTEM_DEBUG", "false").lower() == "true":
    logger.setLevel(logging.DEBUG)
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        "%(asctime)s: %(name)-70s %(levelname)-8s %(message)s", datefmt="%m-%d %H:%M"
    )
else:
    logger.setLevel(logging.INFO)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s: %(levelname)-8s %(message)s", datefmt="%m-%d %H:%M"
    )
handler.setFormatter(formatter)
logger.addHandler(handler)
