from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "JvX Nexus"
    DATABASE_URL: str = "sqlite:///./jvx_hackathon.db"
    class Config:
        env_file = ".env"

settings = Settings()