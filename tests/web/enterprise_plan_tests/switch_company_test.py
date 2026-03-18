import pytest
from playwright.sync_api import expect
from src.web.application import Application


@pytest.mark.smoke
@pytest.mark.web
def test_switch_company_to_free_projects(logged_app: Application):
    logged_app.projects_page.navigate()
    logged_app.projects_page.verify_page_loaded()
    logged_app.projects_page.header.select_company("Free Projects")
    logged_app.page.wait_for_load_state("networkidle")

    expect(logged_app.page.get_by_text("Free plan")).to_be_visible()
    logged_app.projects_page.search_and_get_results("Manufacture light")
    logged_app.projects_page.assert_project_count(0)
