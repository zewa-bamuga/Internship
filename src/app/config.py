from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApiSettings(BaseSettings):
    prefix: str = Field(default="/api")
    cors_origins: list[str] = Field(default=["*"])
    show_docs: bool = Field(default=True)
    auth_uri: str = Field(default="/api/v1/users/authentication/oauth")
    model_config = SettingsConfigDict(env_prefix="API_")


class DatabaseSettings(BaseSettings):
    dsn: str = Field(default=...)
    model_config = SettingsConfigDict(env_prefix="DB_")


class Settings(BaseSettings):
    api: ApiSettings = ApiSettings()
    db: DatabaseSettings = DatabaseSettings()
