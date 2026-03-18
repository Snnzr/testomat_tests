import pytest
from src.web.application import Application
from src.web.components.project_card import Badges

DEMO_PROJECT_NAME = "Manufacture light"
DEFAULT_COMPANY = "QA Club Lviv"
EXPECTED_PLAN = "Enterprise plan"


@pytest.mark.smoke
@pytest.mark.web
def test_projects_page_header(logged_app: Application):
    logged_app.projects_page.navigate()
    logged_app.projects_page.verify_page_loaded()

    logged_app.projects_page.header.check_selected_company(DEFAULT_COMPANY)
    logged_app.projects_page.header.plan_name_should_be(EXPECTED_PLAN)

    logged_app.projects_page.search_and_get_results(DEMO_PROJECT_NAME)
    logged_app.projects_page.assert_project_count(2)
    target_project = logged_app.projects_page.get_project_by_title(DEMO_PROJECT_NAME)
    target_project.assert_has_badge(Badges.CLASSICAL)
