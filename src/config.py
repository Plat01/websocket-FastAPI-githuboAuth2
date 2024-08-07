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

    EXPOSE_PORT: int = 8008

    GITHUB_CLIENT_ID: str ='your-app-id'
    GITHUB_CLIENT_SECRET: str = 'your-app-secret'
    GITHUB_CALLBACK: str = 'github-callback'
    GITHUB_CALLBACK_URL: str = 'http://localhost:8008/github-callback'

    LOGGER_LVL: int = 10  # DEBUG

    SERVICE_PORT: int = 8888
    EXPOSE_REDIS: int = 9876
    SERVICE_HOST: str = "localhost"

    REDIS_HOST: str = 'localhost'
    REDIS_PORT: int = 6379
    REDIS_DATABASE: int = 0


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
