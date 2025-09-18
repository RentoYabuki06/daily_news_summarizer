from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Daily News Summarizer"
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
