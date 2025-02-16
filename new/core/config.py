# mypy: disable-error-code=call-arg

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_PATH = ".env"


class DBSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH, env_file_encoding="utf-8", extra="ignore")

    MYSQL_ROOT_PASSWORD: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str
    DATABASE_URL: str
    ALEMBIC_DATABASE_URL: str


class RabbitSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH, env_file_encoding="utf-8", extra="ignore")

    RABBITMQ_URL: str
    QUEUE_NAME: str


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file=ENV_PATH, env_file_encoding="utf-8", extra="ignore")

    REDIS_HOST: str
    REDIS_PORT: int


db_settings = DBSettings()
rabbitmq_settings = RabbitSettings()
redis_settings = RedisSettings()

print(db_settings)
print(rabbitmq_settings)
print(redis_settings)
