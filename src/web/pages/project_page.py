from typing import Self

from playwright.sync_api import Page, expect

from src.web.components.side_bar import Sidebar


class ProjectPage:
    def __init__(self, page: Page):
        self.page = page
        self.side_bar = Sidebar(page)

    def open_by_id(self, project_id: str) -> Self:
        self.page.goto(f"/projects/{project_id}")
        return self

    def assert_loaded(self) -> Self:
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.page.locator(".mainnav-menu")).to_be_visible(timeout=10000)
        expect(self.page.locator("button.btn-open")).to_be_visible(timeout=10000)
        expect(self.page.locator("h2:visible").first).to_be_visible(timeout=10000)
        return self

    def assert_project_name(self, expected_project_name: str) -> Self:
        expect(self.page.locator(".sticky-header h2")).to_have_text(
            expected_project_name, timeout=10000
        )
        return self

    def close_read_me(self) -> Self:
        close_button = self.page.locator(".back .third-btn:visible").first
        if close_button.count() > 0:
            close_button.click()
        return self

    def create_test_via_popup(self) -> Self:
        self.page.locator(".sticky-header").get_by_role(
            "button", name="Test", exact=True
        ).click()
        return self

    def create_test_suite_via_popup(self) -> Self:
        self.page.locator(".md-icon-chevron-down").click()
        self.page.get_by_text("Collection of test cases").click()
        return self

    def create_first_suite(self, target_suite_name: str) -> Self:
        self.page.locator("[placeholder='First Suite']").fill(target_suite_name)
        suite_button = self.page.get_by_role("button", name="Suite")
        suite_button.click()
        expect(suite_button).to_be_hidden(timeout=10000)
        return self

    def assert_suite_visible(self, test_suite_name: str) -> Self:
        expect(
            self.page.locator(".suites-list-content").get_by_text(test_suite_name)
        ).to_be_visible()
        return self
