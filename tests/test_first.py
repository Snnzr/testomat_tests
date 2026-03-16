import os

import pytest
from faker import Faker
from playwright.sync_api import Page, expect

from tests.support.config import Config

TARGET_PROJECT = "Manufacture light"


@pytest.fixture(scope="function")
def login(page: Page, config: Config):
    page.goto(config.login_url)
    login_user(page, email=config.email, password=config.password)
    expect(page.locator("h2", has_text="Projects")).to_be_visible(timeout=10000)


def test_open_home_page(page: Page):
    page.goto("https://testomat.io")

    expect(page).to_have_title("AI Test Management Tool | Testomat.io")
    expect(page.locator("[href*='sign_in'].login-item")).to_be_visible()
    expect(page.get_by_text("Log in", exact=True)).to_be_visible()


def test_login_with_invalid_creds(page: Page, config: Config):
    open_home_page(page)

    expect(page.locator("[href*='sign_in'].login-item")).to_be_visible()

    page.get_by_text("Log in", exact=True).click()

    login_user(page, email=config.email, password=Faker().password(length=10))

    expect(
        page.locator("#content-desktop").get_by_text("Invalid Email or password.")
    ).to_be_visible()
    expect(page.locator("#content-desktop .common-flash-info")).to_have_text(
        "Invalid Email or password."
    )


def test_search_project_in_company(page: Page, login):
    search_for_project(page, TARGET_PROJECT)

    expect(page.get_by_role("heading", name=TARGET_PROJECT).first).to_be_visible()

    expect(page.locator("ul li h3", has_text=TARGET_PROJECT).first).to_be_visible()


def test_should_be_possible_to_open_free_project(page: Page, login):
    page.locator("#company_id").click()
    page.locator("#company_id").select_option(label="Free Projects")

    search_for_project(page, TARGET_PROJECT)
    expect(page.get_by_role("heading", name=TARGET_PROJECT).first).to_be_hidden()

    expect(page.get_by_text("You have not created any projects yet")).to_be_hidden()


def search_for_project(page: Page, target_project: str):
    expect(page.get_by_role("searchbox", name="Search")).to_be_visible()
    page.locator("#content-desktop #search").fill(target_project)
    page.wait_for_timeout(1000)


def open_home_page(page: Page):
    page.goto(os.getenv("BASE_URL"))


def login_user(page: Page, email: str, password: str):
    page.locator("#content-desktop #user_email").fill(email)
    page.locator("#content-desktop #user_password").fill(password)
    page.get_by_role("button", name="Sign in").click()
