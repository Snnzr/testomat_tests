from urllib.parse import urlparse

from playwright.sync_api import Page

from src.web.components.test_for_suite_popup import TestForSuitePopup
from src.web.components.test_modal import TestModal
from src.web.pages.home_page import HomePage
from src.web.pages.login_page import LoginPage
from src.web.pages.new_projects_page import NewProjectsPage
from src.web.pages.project_page import ProjectPage
from src.web.pages.projects_page import ProjectsPage


class Application:
    def __init__(self, page: Page):
        self.page = page
        self.home_page = HomePage(page)
        self.login_page = LoginPage(page)
        self.projects_page = ProjectsPage(page)
        self.new_projects_page = NewProjectsPage(page)
        self.project_page = ProjectPage(page)
        self.test_for_suite_popup = TestForSuitePopup(page)
        self.test_modal = TestModal(page)

    def clear_cookies_and_local_storage(self):
        """
        Clears browser cookies and localStorage for all known origins
        in the current browser context.
        """
        context = self.page.context
        context.clear_cookies()

        storage_state = context.storage_state()
        origins = {
            origin_entry["origin"]
            for origin_entry in storage_state.get("origins", [])
            if origin_entry.get("origin")
        }

        parsed_url = urlparse(self.page.url or "")
        if parsed_url.scheme in {"http", "https"} and parsed_url.netloc:
            origins.add(f"{parsed_url.scheme}://{parsed_url.netloc}")

        for origin in origins:
            cleanup_page = context.new_page()
            try:
                cleanup_page.goto(origin, wait_until="domcontentloaded")
                cleanup_page.evaluate("() => window.localStorage.clear()")
            finally:
                cleanup_page.close()
