
from aiobotocore.session import get_session
from loguru import logger


class SQSWriter:
    client = None

    async def initiate(self, config):
        logger.info(f" initiating SQS")
        session = get_session()
        self.client = await session._create_client(
            "sqs",
            region_name=config["sqs"]["region"],
            endpoint_url=config["sqs"]["endpoint"],
        )
        logger.info(f" connection SQS  started")

    async def write(self, config, documents):
        for doc in documents:
            return await self.client.send_message(
                QueueUrl=config["sqs"]["queue_url"],
                MessageBody=doc['Messages'][0]['Body'],
                MessageAttributes = doc['Messages'][0]['MessageAttributes']
            )

    async def close_sqs_connection(self) -> None:
        logger.info("Closing sqs connection..")
        await self.client.close()
        logger.info("Closed sqs connection..")