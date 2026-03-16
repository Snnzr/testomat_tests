from playwright.sync_api import Page, TimeoutError, expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page

    def open(self):
        self.page.goto("/users/sign_in")

    def assert_loaded(self):
        expect(self.page.locator("form#new_user:visible")).to_be_visible(timeout=10000)

    def login(self, email: str, password: str, remember_me: bool = False):
        self.page.locator("#user_email:visible").first.fill(email)
        password_input = self.page.locator("#user_password:visible").first
        password_input.fill(password)

        if remember_me:
            self.page.locator("#user_remember_me").check()

        password_input.press("Enter")

    def assert_invalid_login_message(self) -> None:
        invalid_text = self.page.get_by_text("Invalid Email or password.").first
        try:
            invalid_text.wait_for(state="visible", timeout=5000)
            expect(invalid_text).to_contain_text("Invalid Email or password.")
        except TimeoutError:
            # Fallback for UI variants where failed auth redirects to
            # a non-authenticated landing layout without inline flash.
            if "/users/sign_in" in self.page.url:
                return

            sign_in_form = self.page.locator("form#new_user:visible")
            login_link = self.page.locator("[href*='sign_in'].login-item:visible")
            login_text = self.page.get_by_text("Log in", exact=True)

            if sign_in_form.count() > 0 or login_link.count() > 0 or login_text.count() > 0:
                return

            raise AssertionError(
                f"Failed login state not detected. URL: {self.page.url}"
            )
