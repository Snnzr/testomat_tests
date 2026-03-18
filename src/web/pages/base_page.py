from __future__ import annotations

from abc import ABC, abstractmethod

from playwright.sync_api import Page


class BasePage(ABC):
    """Base class for shared page-object helpers."""

    def __init__(self, page: Page):
        self.page = page

    @abstractmethod
    def assert_loaded(self) -> "BasePage":
        """Verify the page is ready for interaction."""

    def wait_for_load(self, timeout: int = 30000) -> "BasePage":
        self.page.wait_for_load_state("domcontentloaded", timeout=timeout)
        return self

    def get_current_url(self) -> str:
        return self.page.url

    def get_title(self) -> str:
        return self.page.title()

    def take_screenshot(self, path: str) -> "BasePage":
        self.page.screenshot(path=path)
        return self

    def scroll_to_top(self) -> "BasePage":
        self.page.evaluate("window.scrollTo(0, 0)")
        return self

    def scroll_to_bottom(self) -> "BasePage":
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        return self
