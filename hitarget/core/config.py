from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "hiTarget-API"
    API_V1_PREFIX: str = "/api/v1"

    MONGODB_URI: str = "mongodb://127.0.0.1:27017/hitarget"
    MONGODB_MAX_POOL_SIZE = 10
    MONGODB_MIN_POOL_SIZE = 1

    class Config:
        case_sensitive = True


settings = Settings()
