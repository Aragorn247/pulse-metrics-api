from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Pulse Metrics API"
    DEBUG: bool = True
    DATABASE_URL: str
    REDIS_URL: str

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()