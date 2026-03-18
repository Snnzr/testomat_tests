import pytest

pytest.importorskip("httpx")

from src.api.client import ApiClient
from src.api.models import Project, ProjectsResponse


class TestAuthentication:
    def test_login_with_valid_token(self, api_client: ApiClient):
        jwt_token = api_client._authenticate()

        assert jwt_token is not None
        assert isinstance(jwt_token, str)
        assert len(jwt_token) > 0

    def test_jwt_token_is_cached(self, api_client: ApiClient):
        first_token = api_client._authenticate()
        second_token = api_client._authenticate()

        assert first_token == second_token


class TestGetProjects:
    def test_get_projects_returns_response(self, api_client: ApiClient):
        response = api_client.get_projects()

        assert response is not None
        assert isinstance(response, ProjectsResponse)

    def test_get_projects_returns_list_of_projects(self, api_client: ApiClient):
        response = api_client.get_projects()

        assert isinstance(response.data, list)
        if len(response) > 0:
            assert isinstance(response[0], Project)

    def test_project_has_required_attributes(self, api_client: ApiClient):
        response = api_client.get_projects()

        if len(response) > 0:
            project = response[0]
            assert project.id is not None
            assert project.type == "project"
            assert project.title is not None
            assert project.status is not None

    def test_projects_response_is_iterable(self, api_client: ApiClient):
        projects = api_client.get_projects()

        for project in projects:
            assert project.id
            assert project.title is not None
