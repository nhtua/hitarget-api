import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from .config import settings


class DBEngine:
    client: AsyncIOMotorClient = None


dbe = DBEngine()


async def get_database(db_name: str = None) -> AsyncIOMotorDatabase:
    return dbe.client.get_default_database(settings.MONGODB_NAME
                                           if db_name is None else db_name)


async def connect():
    logging.info('Connecting to MongoDB')
    dbe.client = AsyncIOMotorClient(settings.MONGODB_URL,
                                   maxPoolSize=settings.MONGODB_MAX_POOL_SIZE,
                                   minPoolSize=settings.MONGODB_MIN_POOL_SIZE)
    logging.info('MongoDB Connected!')
    return dbe.client


async def disconnect():
    dbe.client.close()
    logging.info('MongoDB Disconnected!')
