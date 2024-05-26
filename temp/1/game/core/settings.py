import os
from typing import Literal

from pydantic import SecretStr
from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__name__)))

LOG_LEVEL = Literal[
    "CRITICAL",
    "FATAL",
    "ERROR",
    "WARN",
    "WARNING",
    "INFO",
    "DEBUG",
    "NOTSET",
]


class Base(BaseSettings):
    class Config:
        """Settings for reading environment variables from a file.

        env_file - The path to the environment, to run locally
        """

        env_nested_delimiter = "__"
        env_file = os.path.join(BASE_DIR, ".env_www")
        enf_file_encoding = "utf-8"
        extra = "ignore"


class LogSettings(Base):
    """Setting logging.

    level (str, optional): The level of logging. Defaults to "INFO".
    guru (bool, optional): Whether to enable guru mode. Defaults to True.
    traceback (bool, optional): Whether to include tracebacks in logs. Defaults to True.
    """

    level: LOG_LEVEL = "INFO"
    guru: bool = True
    traceback: bool = True


class RabbitMQSettings(Base):
    rabbit_user: str
    rabbit_password: SecretStr
    rabbit_host: str
    rabbit_port: int

    def dsn(self, show_secret: bool = False) -> str:
        """Returns the connection URL as a string.

        Args:
            show_secret (bool, optional): Whether to show the secret. Defaults to False.

        Returns:
            str: The connection URL.
        """
        return "amqp://{user}:{password}@{host}:{port}/".format(
            user=self.rabbit_user,
            password=(
                self.rabbit_password.get_secret_value()
                if show_secret
                else self.rabbit_password
            ),
            host=self.rabbit_host,
            port=self.rabbit_port,
        )


class PostgresSettings(Base):
    """Settings for PostgresSQL database connections.

    Attributes:
        postgres_db: The name of the database.
        postgres_user: The username for the database.
        postgres_password: The password for the database.
        postgres_host: The hostname or IP address of the database server.
        postgres_port: The port number of the database server.
        postgres_schema: The name of the schema to use.

    Methods:
        dsn: Returns the connection URL as a string.
    """

    postgres_db: str
    postgres_user: str
    postgres_password: SecretStr
    postgres_host: str
    postgres_port: str
    postgres_schema: str

    def dsn(self, show_secret: bool = False) -> str:
        """Returns the connection URL as a string.

        Args:
            show_secret (bool, optional): Whether to show the secret. Defaults to False.

        Returns:
            str: The connection URL.
        """
        return "postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}".format(
            user=self.postgres_user,
            password=(
                self.postgres_password.get_secret_value()
                if show_secret
                else self.postgres_password
            ),
            host=self.postgres_host,
            port=self.postgres_port,
            db=self.postgres_db,
        )
