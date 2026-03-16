import pytest
from playwright.sync_api import Page
from src.web.pages.home_page import HomePage
from src.web.pages.login_page import LoginPage
from src.web.pages.projects_page import ProjectsPage

from tests.support.config import Config


def open_login_page(page: Page) -> LoginPage:
    home_page = HomePage(page)
    home_page.open()
    home_page.assert_loaded()
    home_page.click_login()

    login_page = LoginPage(page)
    login_page.assert_loaded()
    return login_page


@pytest.mark.parametrize(
    "data_pair",
    [
        pytest.param(
            lambda config, faker: (config.email, config.password, True),
            id="eq_valid_credentials",
        ),
        pytest.param(
            lambda config, faker: (
                faker.pystr(min_chars=8, max_chars=12),
                config.password,
                False,
            ),
            id="eq_invalid_email_format",
        ),
        pytest.param(
            lambda config, faker: (faker.unique.email(), config.password, False),
            id="eq_unregistered_email",
        ),
        pytest.param(
            lambda config, faker: (config.email, faker.password(length=4), False),
            id="eq_wrong_password",
        ),
        pytest.param(
            lambda config, faker: ("", "", False),
            id="eq_empty_credentials",
        ),
        pytest.param(
            lambda config, faker: ("", config.password, False),
            id="bva_email_empty",
        ),
        pytest.param(
            lambda config, faker: (
                f"{faker.pystr(min_chars=245, max_chars=245)}@x.com",
                config.password,
                False,
            ),
            id="bva_email_too_long",
        ),
        pytest.param(
            lambda config, faker: (config.email, "", False),
            id="bva_password_empty",
        ),
        pytest.param(
            lambda config, faker: (config.email, "a", False),
            id="bva_password_min_length",
        ),
    ],
)
def test_login_functionality(page: Page, config: Config, faker, data_pair):
    email, password, should_login = data_pair(config, faker)

    login_page = open_login_page(page)
    login_page.login(email=email, password=password)

    if should_login:
        ProjectsPage(page).assert_signed_in()
    else:
        login_page.assert_invalid_login_message()
