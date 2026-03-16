from faker import Faker
from playwright.sync_api import Page
from src.web.application import Application


def test_new_project_creation(page: Page, login, app: Application):
    target_project_name = Faker().company()

    app.projects_page.header.click_create()

    (
        app.new_projects_page.assert_loaded()
        .fill_project_title(target_project_name)
        .click_create()
    )

    (
        app.project_page.assert_loaded()
        .assert_project_name(target_project_name)
        .close_read_me()
    )

    (app.project_page.side_bar.assert_loaded().click_logo().expect_tab_active("Tests"))
