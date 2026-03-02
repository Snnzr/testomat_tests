import pytest
from faker import Faker
from playwright.sync_api import Page

from src.web.pages.HomePage import HomePage
from src.web.pages.LoginPage import LoginPage
from src.web.pages.ProjectsPage import ProjectsPage
from tests.conftest import Config

fake = Faker()


@pytest.mark.parametrize("email, password", [
    (fake.email(), fake.password(length=10)),
    (fake.email(), fake.password(length=8)),
])
def test_login_invalid(page: Page, configs: Config, email, password):
    home_page = HomePage(page)
    home_page.open()
    home_page.is_loaded()
    home_page.click_login()

    login_page = LoginPage(page)
    login_page.is_loaded()
    login_page.login(email=email, password=password)
    login_page.invalid_login_message_visible()


def test_login_with_valid_creds(page: Page, configs: Config):
    home_page = HomePage(page)
    home_page.open()
    home_page.is_loaded()
    home_page.click_login()

    login_page = LoginPage(page)
    login_page.is_loaded()
    login_page.login(email=configs.email, password=configs.password)

    ProjectsPage(page).is_loaded()
