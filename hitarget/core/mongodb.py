import logging
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from .config import settings


class DBEngine:
    client: AsyncIOMotorClient = None


dbe = DBEngine()


# Endpoint dependency should not have params to avoid it showing up in document
async def get_database() -> AsyncIOMotorDatabase:
    return dbe.client.get_default_database(settings.MONGODB_NAME)


async def connect():
    logging.info('Connecting to MongoDB')
    dbe.client = AsyncIOMotorClient(settings.MONGODB_URL,
                                   maxPoolSize=settings.MONGODB_MAX_POOL_SIZE,
                                   minPoolSize=settings.MONGODB_MIN_POOL_SIZE,
                                   tls=settings.MONGODB_TLS,
                                   tlsAllowInvalidCertificates=settings.MONGODB_BYPASS_TLS)
    logging.info('MongoDB Connected!')
    return dbe.client


async def disconnect():
    dbe.client.close()
    logging.info('MongoDB Disconnected!')
