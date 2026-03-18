import pytest

from tests.support.config import Config


@pytest.fixture(scope="session")
def api_client(configs: Config):
    if not configs.testomat_token:
        pytest.skip("TESTOMAT_TOKEN is not configured")

    pytest.importorskip("httpx")
    from src.api.client import ApiClient

    client = ApiClient(
        base_url=configs.app_base_url,
        api_token=configs.testomat_token,
    )
    client._authenticate()
    yield client
    client.close()
