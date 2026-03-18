import pytest
from faker import Faker
from src.web.application import Application

fake = Faker()

invalid_login_test_data = [
    pytest.param(fake.email(), fake.password(length=10), id="unregistered_valid_email"),
    pytest.param(
        fake.user_name(), fake.password(length=10), id="email_missing_at_symbol"
    ),
    pytest.param("invalid@", fake.password(length=10), id="email_missing_domain"),
    pytest.param(
        "@domain.com", fake.password(length=10), id="email_missing_local_part"
    ),
    pytest.param("user@@domain.com", fake.password(length=10), id="email_double_at"),
    pytest.param(
        "user name@domain.com", fake.password(length=10), id="email_with_space"
    ),
    pytest.param(fake.email(), "", id="empty_password"),
    pytest.param(fake.email(), "   ", id="password_only_spaces"),
    pytest.param(fake.email(), "ab", id="password_2_chars"),
    pytest.param(fake.email(), "a" * 256, id="password_256_chars"),
    pytest.param("", "", id="both_empty"),
    pytest.param("", fake.password(length=10), id="empty_email"),
    pytest.param("a@b.c", fake.password(length=10), id="min_valid_email_format"),
    pytest.param(
        f"{'a' * 64}@{'b' * 63}.com", fake.password(length=10), id="max_length_email"
    ),
    pytest.param(fake.email(), "pass<script>alert(1)</script>", id="xss_in_password"),
    pytest.param(
        fake.email(), "pass'; DROP TABLE users;--", id="sql_injection_password"
    ),
]


@pytest.mark.regression
@pytest.mark.web
@pytest.mark.parametrize("email, password", invalid_login_test_data)
def test_login_invalid(app: Application, email: str, password: str):
    app.login_page.open()
    app.login_page.assert_loaded()
    app.login_page.login(email, password)
    app.login_page.assert_invalid_login_message()


@pytest.mark.smoke
@pytest.mark.web
def test_login_with_valid_creds(logged_app: Application):
    logged_app.projects_page.verify_page_loaded()
