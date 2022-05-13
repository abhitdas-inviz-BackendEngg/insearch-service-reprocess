from loguru import logger
import asyncio
import logging
import sys
from datetime import datetime

from src.main.config.logging import InterceptHandler, Formatter
from src.main.config.parser import load_config
from src.main.util.invalid_reprocess_indexer import InvalidReprocessIndexer

LOGGING_LEVEL = logging.INFO


logging.basicConfig(
    handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
)
logger.configure(
    handlers=[
        {"sink": sys.stdout, "level": LOGGING_LEVEL, "format": Formatter().format}
    ]
)
logger.info(' Starting job at {}'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
config = load_config()

loop = asyncio.get_event_loop()
loop.run_until_complete(InvalidReprocessIndexer().start(config))
logger.info(' Finshing job at {}'.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))