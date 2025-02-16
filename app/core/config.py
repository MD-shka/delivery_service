from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = "/projects/delivery_service/.env"

class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH, env_file_encoding="utf-8")

    MYSQL_ROOT_PASSWORD: str = model_config.get("MYSQL_ROOT_PASSWORD")
    MYSQL_USER: str = model_config.get("MYSQL_USER")
    MYSQL_PASSWORD: str = model_config.get("MYSQL_PASSWORD")
    MYSQL_DATABASE: str = model_config.get("MYSQL_DATABASE")
    DATABASE_URL: str = model_config.get("DATABASE_URL")


class RabbitSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH, env_file_encoding="utf-8")

    RABBITMQ_URL: str = model_config.get("RABBITMQ_URL")


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH, env_file_encoding="utf-8")

    REDIS_HOST: str = model_config.get("REDIS_HOST")
    REDIS_PORT: int = model_config.get("REDIS_PORT")


db_settings = DBSettings()
rabbitmq_settings = RabbitSettings()
redis_settings = RedisSettings()
