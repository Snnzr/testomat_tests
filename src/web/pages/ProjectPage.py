from typing import Self

from playwright.sync_api import Page, expect

# from src.web.components import SideBar
from src.web.components import SideBar


class ProjectPage:
    def __init__(self, page: Page):
        self.page = page
        self.side_bar = SideBar(page)

    def is_loaded(self) -> Self:
        self.page.wait_for_load_state("domcontentloaded")
        expect(self.page.locator(".mainnav-menu")).to_be_visible(timeout=10000)
        expect(self.page.locator("button.btn-open")).to_be_visible(timeout=10000)
        expect(self.page.locator("h2:visible").first).to_be_visible(timeout=10000)
        return self

    def empty_project_name_is(self, expected_project_name: str) -> Self:
        expect(self.page.locator(".sticky-header h2")).to_have_text(expected_project_name, timeout=10000)
        return self

    def close_read_me(self) -> Self:
        close_button = self.page.locator(".back .third-btn:visible").first
        if close_button.count() > 0:
            close_button.click()
        return self
