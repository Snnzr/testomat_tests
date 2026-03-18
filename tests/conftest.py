import pytest
from playwright.sync_api import Page, expect
from src.web.application import Application

from tests.support.config import Config, load_config

pytest_plugins = [
    "tests.fixtures.config",
    "tests.fixtures.api",
    "tests.fixtures.app",
]


@pytest.fixture(scope="session")
def config() -> Config:
    return load_config()


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    return Application(page)


@pytest.fixture(scope="function")
def login(app: Application, config: Config):
    app.login_page.open()
    app.login_page.assert_loaded()
    app.login_page.login(config.email, config.password)
    app.projects_page.navigate()
    expect(app.page.locator("h2", has_text="Projects")).to_be_visible(timeout=10000)
