import pytest
from playwright.sync_api import Page

from src.web.pages.HomePage import HomePage
from src.web.pages.LoginPage import LoginPage
from src.web.pages.ProjectsPage import ProjectsPage
from tests.conftest import Config


def open_login_page(page: Page) -> LoginPage:
    home_page = HomePage(page)
    home_page.open()
    home_page.is_loaded()
    home_page.click_login()

    login_page = LoginPage(page)
    login_page.is_loaded()
    return login_page


@pytest.mark.parametrize(
    "data_pair",
    [
        pytest.param(
            lambda configs, faker: (configs.email, configs.password, True),
            id="eq_valid_credentials",
        ),
        pytest.param(
            lambda configs, faker: (faker.pystr(min_chars=8, max_chars=12), configs.password, False),
            id="eq_invalid_email_format",
        ),
        pytest.param(
            lambda configs, faker: (faker.unique.email(), configs.password, False),
            id="eq_unregistered_email",
        ),
        pytest.param(
            lambda configs, faker: (configs.email, faker.password(length=4), False),
            id="eq_wrong_password",
        ),
        pytest.param(
            lambda configs, faker: ("", "", False),
            id="eq_empty_credentials",
        ),
        pytest.param(
            lambda configs, faker: ("", configs.password, False),
            id="bva_email_empty",
        ),
        pytest.param(
            lambda configs, faker: (f"{faker.pystr(min_chars=245, max_chars=245)}@x.com", configs.password, False),
            id="bva_email_too_long",
        ),
        pytest.param(
            lambda configs, faker: (configs.email, "", False),
            id="bva_password_empty",
        ),
        pytest.param(
            lambda configs, faker: (configs.email, "a", False),
            id="bva_password_min_length",
        ),
    ],
)
def test_login_functionality(page: Page, configs: Config, faker, data_pair):
    email, password, should_login = data_pair(configs, faker)

    login_page = open_login_page(page)
    login_page.login(email=email, password=password)

    if should_login:
        ProjectsPage(page).is_loaded()
    else:
        login_page.invalid_login_message_visible()
