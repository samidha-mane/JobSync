from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str
    adzuna_app_id: str
    adzuna_app_key: str

    class Config:
        env_file = ".env"


settings = Settings()