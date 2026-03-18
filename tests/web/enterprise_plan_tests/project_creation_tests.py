import pytest
from faker import Faker
from src.web.application import Application


@pytest.mark.smoke
@pytest.mark.web
def test_new_project_creation_and_test_popup(logged_app: Application):
    target_project_name = Faker().company()

    (
        logged_app.new_projects_page
        .open()
        .assert_loaded()
        .fill_project_title(target_project_name)
        .click_create()
    )

    (
        logged_app.project_page
        .assert_loaded()
        .assert_project_name(target_project_name)
        .close_read_me()
    )

    logged_app.project_page.side_bar.assert_loaded().click_logo().expect_tab_active(
        "Tests"
    )


@pytest.mark.smoke
@pytest.mark.web
def test_open_project_and_create_test_suite_from_side_bar(
    api_client, logged_app: Application
):
    all_projects = api_client.get_projects()
    target_project_id = all_projects[0].id

    logged_app.project_page.open_by_id(target_project_id).assert_loaded()
    logged_app.project_page.side_bar.assert_loaded()
    logged_app.project_page.create_test_suite_via_popup()

    test_name = Faker().sentence()
    logged_app.test_modal.assert_loaded("Suite").set_title(test_name).save()
    logged_app.project_page.assert_suite_visible(test_name)
