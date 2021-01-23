from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "hiTarget-API"
    API_V1_PREFIX: str = "/api/v1"

    MONGODB_URL: str = "mongodb://127.0.0.1:27017/"
    MONGODB_NAME: str = "hitarget"
    MONGODB_MAX_POOL_SIZE = 10
    MONGODB_MIN_POOL_SIZE = 1

    JWT_ISSUER: str = "hiTargetV1"
    JWT_ALGORITHM: str = "HS256"
    JWT_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # one week

    class Config:
        case_sensitive = True


settings = Settings()
