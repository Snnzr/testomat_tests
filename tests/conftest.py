import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from src.web.application import Application
from tests.support.browser_state import reset_page_state
from tests.support.config import Config, load_config


@pytest.fixture(scope="session")
def config() -> Config:
    return load_config()


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    return Application(page)


@pytest.fixture(scope="session")
def page(shared_page: Page) -> Page:
    """
    Override pytest-playwright default page fixture to reuse one page
    across the full test session.
    """
    return shared_page


@pytest.fixture(scope="function", autouse=True)
def reset_shared_page_state(page: Page, config: Config):
    """
    Keep one reused page for the whole run, but reset browser state
    before each test to avoid cross-test contamination.
    """
    reset_page_state(page, config)


@pytest.fixture(scope="session")
def shared_browser(browser: Browser) -> Browser:
    """Session-level browser instance for tests that want browser reuse."""
    return browser


@pytest.fixture(scope="session")
def shared_context(
    shared_browser: Browser, browser_context_args: dict
) -> BrowserContext:
    """
    Session-level browser context for tests that want context reuse.
    Uses the same context args as the default playwright fixtures.
    """
    existing_contexts = shared_browser.contexts
    created_context = False

    if existing_contexts:
        context = existing_contexts[0]
    else:
        context = shared_browser.new_context(**browser_context_args)
        created_context = True

    yield context
    if created_context:
        context.close()


@pytest.fixture(scope="session")
def shared_page(shared_context: BrowserContext) -> Page:
    """Session-level page for tests that want page reuse."""
    existing_pages = shared_context.pages
    created_page = False

    if existing_pages:
        page = existing_pages[0]
    else:
        page = shared_context.new_page()
        created_page = True

    yield page
    if created_page:
        page.close()


@pytest.fixture(scope="session")
def shared_app(shared_page: Page) -> Application:
    """Application wrapper bound to the shared page."""
    return Application(shared_page)


@pytest.fixture(scope="function")
def login(app: Application, config: Config):
    page = app.page

    for attempt in range(2):
        app.login_page.open()

        sign_in_form = page.locator("form#new_user:visible")
        if not sign_in_form.first.is_visible(timeout=10000):
            # Shared-page runs can occasionally land on app root or a cached state
            # right after reset; retry loading the sign-in page once.
            app.login_page.open()

        if sign_in_form.first.is_visible(timeout=5000):
            app.login_page.login(config.email, config.password)

        app.projects_page.navigate()
        try:
            app.projects_page.verify_page_loaded()
            return
        except AssertionError:
            if attempt == 1:
                raise

            # Hard reset state before one final retry.
            reset_page_state(page, config)


@pytest.fixture(scope="session")
def shared_login(shared_app: Application, config: Config):
    """
    One-time login for shared-page flows.
    Useful only when tests are designed to run with shared state.
    """
    shared_app.login_page.open()
    shared_app.login_page.assert_loaded()
    shared_app.login_page.login(config.email, config.password)
    shared_app.projects_page.navigate()
    shared_app.projects_page.verify_page_loaded()
