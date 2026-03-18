import pytest
from src.web.application import Application

from tests.fixtures.cookie_helper import CookieHelper
from tests.support.config import Config


@pytest.fixture(scope="function")
def logged_app(app: Application, login) -> Application:
    return app


@pytest.fixture(scope="function")
def cookies(logged_app: Application) -> CookieHelper:
    return CookieHelper(logged_app.page.context)


@pytest.fixture(scope="function")
def free_project_app(app: Application, login, config: Config) -> Application:
    app.projects_page.navigate()
    app.projects_page.verify_page_loaded()
    app.projects_page.header.select_company("Free Projects")
    app.page.wait_for_load_state("networkidle")
    return app
