from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):

    database_password: str = ""
    database_user: str = ""
    database_port: str = "5432"
    database_name: str = ""
    database_host: str = "localhost"

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def async_database_url(self) -> str:
        return f"postgresql+asyncpg://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"

    @property
    def sync_database_url(self) -> str:
        return f"postgresql+psycopg2://{self.database_user}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"

config = Config()


if __name__ == "__main__":
    print(config.async_database_url)
