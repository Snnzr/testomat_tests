# Testomat Tests

UI end-to-end test suite for Testomat built with `pytest` and Playwright.

## Stack

- Python 3.14
- `uv` for dependency management
- `pytest`
- `playwright`
- `pytest-playwright`
- `python-dotenv`
- `faker`
- `ruff`

## Project Structure

```text
testomat_tests/
|-- src/
|   |-- web/
|   |   |-- application.py
|   |   |-- components/
|   |   `-- pages/
|   `-- data_type_experiments/
|-- tests/
|   |-- support/
|   |-- web/
|   |-- conftest.py
|   `-- test_first.py
|-- .env
|-- pyproject.toml
|-- pytest.ini
`-- uv.lock
```

## Environment Variables

Create a `.env` file in the project root with:

```env
BASE_URL=
BASE_APP_URL=
EMAIL=
PASSWORD=
```

## Setup

Install dependencies with `uv`:

```powershell
uv sync
```

If Playwright browsers are not installed yet:

```powershell
uv run playwright install
```

## Run Tests

Run the full suite:

```powershell
uv run pytest tests
```

Run a single test module:

```powershell
uv run pytest tests\web\test_login_page.py
```

Run tests by marker:

```powershell
uv run pytest -m smoke
```

Run linting and formatting:

```powershell
uv run ruff check .
uv run ruff format .
```

## Notes

- Test discovery is configured in [pytest.ini](C:/Users/snihu/PycharmProjects/testomat_tests/pytest.ini).
- The suite currently runs in headed mode by default via `pytest.ini`.
- Shared fixtures live in [tests/conftest.py](C:/Users/snihu/PycharmProjects/testomat_tests/tests/conftest.py).
- Shared non-fixture test helpers live in [tests/support](C:/Users/snihu/PycharmProjects/testomat_tests/tests/support).

## Verification

Current status after the latest refactor and `uv` migration:

- `uv run pytest tests`
- Result: `15 passed`
