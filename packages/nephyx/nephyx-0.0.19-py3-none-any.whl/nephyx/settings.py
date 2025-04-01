from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class NephyxBaseSettings(BaseSettings):

    model_config = SettingsConfigDict(
        env_prefix="APP_",
        env_file=".env",
    )

    DATABASE_HOST: str = "localhost"
    DATABASE_PORT: str = "5432"
    DATABASE_NAME: str
    DAYABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_URL: PostgresDsn | None = None

    @field_validator("DATABASE_URL")
    @classmethod
    def assemble_database_url(cls, v: PostgresDsn | None, values):
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=values.data.get("database_user"),
            password=values.data.get("database_password"),
            host=values.data.get("database_host"),
            port=int(values.data.get("database_port")),
            path=values.data.get("database_name"),
        )
