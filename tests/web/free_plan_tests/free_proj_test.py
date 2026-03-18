import pytest
from playwright.sync_api import expect
from src.web.application import Application


@pytest.mark.smoke
@pytest.mark.web
def test_free_plan_empty_state(free_project_app: Application):
    expect(free_project_app.page.get_by_text("Free plan")).to_be_visible()
    free_project_app.projects_page.search_and_get_results("Manufacture light")
    free_project_app.projects_page.assert_project_count(0)
