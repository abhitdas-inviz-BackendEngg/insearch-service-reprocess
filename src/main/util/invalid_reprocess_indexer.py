import asyncio

from loguru import logger

from src.main.util.mongo_repo import MongoDB
from src.main.util.sqs_writer import SQSWriter


class InvalidReprocessIndexer:
    async def start(self, config: dict, batch_size: int = 10):
        logger.info("Starting Indexing job .....")

        mongo_db = MongoDB()
        await mongo_db.initiate(config)
        invalidated_docs = await mongo_db.find_invalidated_docs(config)

        sqs_writer = SQSWriter()
        await sqs_writer.initiate(config)

        logger.info("Sending data to SQS started...")
        res = await asyncio.gather(*[sqs_writer.write(config, invalidated_docs[idx:idx+batch_size]) for idx in range(0,len(invalidated_docs),batch_size)])

        logger.info(f"Total messages sent {len(invalidated_docs)}")

        await mongo_db.close_mongo_connection()
        await sqs_writer.close_sqs_connection()
