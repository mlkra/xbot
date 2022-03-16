# Copyright (C) 2022  Michał Krasoń
from pydantic import BaseSettings


class _Settings(BaseSettings):  # pylint: disable=too-few-public-methods
    db_path: str = "xbot.db"
    xkom_url: str = "http://x-kom.pl"
    xkom_api_url: str = "https://mobileapi.x-kom.pl"
    smtp_host: str = "localhost"
    smtp_port: int = 1025


settings = _Settings()
