from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "hiTarget-API"
    API_V1_PREFIX: str = "/api/v1"

    class Config:
        case_sensitive = True


settings = Settings()
