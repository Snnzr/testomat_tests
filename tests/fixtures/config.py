import pytest

from tests.support.config import Config, load_config


@pytest.fixture(scope="session")
def configs() -> Config:
    return load_config()
