from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

class MongoDB:
    client: AsyncIOMotorClient = None

    async def initiate(self, config):
        logger.info(f" initiating Mongo")

        db = config["source"]["documentdb"]
        db_uri = f"mongodb://{db['user']}:{db['pass']}@{db['host']}:{db['port']}/?replicaSet=rs0&readPreference=secondaryPreferred&retryWrites=false"
        # db_uri = f"mongodb+srv://{db['user']}:{db['pass']}@{db['host']}/?retryWrites=true&w=majority"

        self.client = AsyncIOMotorClient(
            str(db_uri),
            maxPoolSize=21,
            minPoolSize=1,
            # ssl=True,
            # ssl_cert_reqs=ssl.CERT_REQUIRED,
            # ssl_ca_certs=SSL_CA_CERTS,
        )
        logger.info(f" connection Mongo  started")

    async def find_invalidated_docs(self, config):
        invalidated_docs = []
        db_config = config["source"]["documentdb"]
        col = self.client[db_config['db_name']][db_config['source_collection']]

        async for document in col.find().sort('updated_date'):
            invalidated_docs.append(document)
        return invalidated_docs

    async def close_mongo_connection(self) -> None:
        logger.info("Closing the mongodb connection..")
        self.client.close()
        logger.info("Mongodb connection closed！")
