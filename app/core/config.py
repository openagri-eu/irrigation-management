from typing import Optional, Any
from pydantic import field_validator
from pydantic_settings import SettingsConfigDict, BaseSettings
from os import path


class Settings(BaseSettings):

    PROJECT_ROOT: str = path.dirname(path.dirname(path.realpath(__file__)))

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB_PORT: int
    POSTGRES_DB: str

    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    KEY: str = "27smVa9g6blmGY0_fJKvuG7elrQ6gapei2cJgaoAcskw"

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    def assemble_db_connection(self, v: Optional[str], values) -> Any:
        if isinstance(v, str):
            return v

        url = f'postgresql://{values.data.get("POSTGRES_USER")}:{values.data.get("POSTGRES_PASSWORD")}' \
              f'@/{values.data.get("POSTGRES_DB")}?host=localhost'

        return url

    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


settings = Settings()
