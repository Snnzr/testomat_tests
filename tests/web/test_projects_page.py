from src.web.application import Application
from src.web.components.project_card import Badges


def test_projects_page_header(app: Application, login):
    """Test page header functionality"""
    app.projects_page.navigate()

    app.projects_page.verify_page_loaded()

    app.projects_page.header.check_selected_company("QA Club Lviv")
    app.projects_page.header.plan_name_should_be("Enterprise plan")

    target_project_name = "Manufacture light"
    app.projects_page.search_and_get_results(target_project_name)
    app.projects_page.assert_project_count(2)
    target_project = app.projects_page.get_project_by_title(target_project_name)
    target_project.assert_has_badge(Badges.CLASSICAL)
