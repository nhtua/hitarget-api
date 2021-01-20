from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "hiTarget-API"

    class Config:
        case_sensitive = True


settings = Settings()
