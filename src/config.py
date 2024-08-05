from pydantic import RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore"
    )

    HOST: str = "localhost"
    PORT: int = 8888

    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str
    GITHUB_CALLBACK_URL: str = 'github-callback'

    LOGGER_LVL: int = 10  # DEBUG

    SERVICE_PORT: int = 8888
    EXPOSE_REDIS: int = 9876
    SERVICE_HOST: str = "localhost"

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_DATABASE: int


    @property
    def REDIS_URL(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis",
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            path=f"/{self.REDIS_DATABASE}"
        )


SETTINGS = Settings()


if __name__ == '__main__':
    pass
