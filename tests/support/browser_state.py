from playwright.sync_api import Page

from tests.support.config import Config


def reset_page_state(page: Page, config: Config) -> None:
    page.context.clear_cookies()

    for url in (config.base_url, config.login_url):
        if not url:
            continue
        page.goto(url, wait_until="domcontentloaded")
        page.evaluate(
            "() => { window.localStorage.clear(); window.sessionStorage.clear(); }"
        )

    page.goto("about:blank")
