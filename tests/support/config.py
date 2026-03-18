import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Config:
    base_url: str
    app_base_url: str
    email: str
    password: str
    testomat_token: str | None = None

    @property
    def login_url(self) -> str:
        return self.app_base_url


def load_config() -> Config:
    return Config(
        base_url=os.getenv("BASE_URL"),
        app_base_url=os.getenv("BASE_APP_URL"),
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
        testomat_token=os.getenv("TESTOMAT_TOKEN"),
    )
