from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    user: str = Field(..., env="POSTGRES_USER")
    password: str = Field(..., env="POSTGRES_PASSWORD")
    port: str = Field(..., env="POSTGRES_PORT")
    database: str = Field(..., env="POSTGRES_DB")
    host: str = Field(..., env="POSTGRES_HOST")

    class Config:
        env_prefix = ""
        case_sentive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'

