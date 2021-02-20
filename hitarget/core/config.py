from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "hiTarget-API"
    API_V1_PREFIX: str = "/api/v1"
    API_PORT: int = "5000"
    API_HOST: str = "0.0.0.0"
    API_ALLOWED_HOSTS = "*"

    MONGODB_URL: str = "mongodb://127.0.0.1:27017/"
    MONGODB_NAME: str = "hitarget-test"
    MONGODB_MAX_POOL_SIZE = 10
    MONGODB_MIN_POOL_SIZE = 1
    MONGODB_TLS = False
    MONGODB_BYPASS_TLS = True  # tlsAllowInvalidCertificates=True

    JWT_ISSUER: str = "hiTargetV1"
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET: str = "Z-chZ4$tpB?u-%wnBxuc"
    JWT_TOKEN_PREFIX = "Bearer"
    JWT_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # one day

    ROUTINE_MAX_SECONDS: int = 60 * 60 * 8  # 8 hours
    ROUTINE_MAX_LIST: int = 100

    class Config:
        case_sensitive = True


settings = Settings()
