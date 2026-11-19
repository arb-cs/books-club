from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from api.clients.auth_client import AuthClient
from api.clients.users_client import UsersClient
from api.models.requests.auth_user_request import AuthUserRequest
from api.models.responses.auth_user_response import AuthUserResponse
from api.models.responses.user_response import UserResponse
from assertions.common import should_have_status
from assertions.errors import should_have_validation_error
from factories.auth_factory import AuthFactory
from fixtures.models import UserContext


@allure.feature("Authentication")
@allure.story("User Authentication")
@allure.severity(Severity.CRITICAL)
@pytest.mark.api
@pytest.mark.authorization
class TestUserAuthentication:

    @allure.title("User can authenticate")
    def test_user_can_authenticate(
        self, registered_user: UserContext, auth_client: AuthClient
    ):
        credentials = AuthUserRequest(
            username=registered_user.registration_request.username,
            password=registered_user.registration_request.password,
        )

        response = auth_client.authenticate(credentials)

        should_have_status(response, HTTPStatus.OK)
        authenticated = AuthUserResponse.model_validate(response.json())

        assert authenticated.access
        assert authenticated.refresh
        assert authenticated.access.count(".") == 2
        assert authenticated.refresh.count(".") == 2

    @allure.title("Authenticated user can access protected resource")
    def test_authenticated_user_can_access_protected_resource(
        self,
        authenticated_user: UserContext,
    ):
        users_client = UsersClient(token=authenticated_user.auth.access)

        response = users_client.get_user()

        should_have_status(response, HTTPStatus.OK)
        user = UserResponse.model_validate(response.json())
        assert authenticated_user.registration_request.username == user.username

    @allure.title(
        "Verify a refresh token can generate a new access and refresh token pair"
    )
    def test_refresh_token_can_generate_new_token_pair(
        self, authenticated_user: UserContext
    ):
        auth_client = AuthClient()
        refresh_request = AuthFactory.build_refresh(
            refresh=authenticated_user.auth.refresh
        )

        response = auth_client.refresh_token(refresh_request)

        should_have_status(response, HTTPStatus.OK)
        new_tokens = AuthUserResponse.model_validate(response.json())

        assert new_tokens.access
        assert new_tokens.refresh

        assert new_tokens.access != authenticated_user.auth.access
        assert new_tokens.refresh != authenticated_user.auth.refresh

        assert new_tokens.access.count(".") == 2
        assert new_tokens.refresh.count(".") == 2

    @allure.title("Verify a username cannot be blank")
    def test_username_cannot_be_blank(self, auth_client: AuthClient):
        credentials = AuthFactory.build(
            username="",
            password="Test12345",
        )

        response = auth_client.authenticate(credentials)

        should_have_status(response, HTTPStatus.BAD_REQUEST)
        should_have_validation_error(
            response,
            field="username",
            message="This field may not be blank.",
        )

    @allure.title("Verify a password cannot be blank")
    def test_password_cannot_be_blank(self, auth_client: AuthClient):
        credentials = AuthFactory.build(
            username="JonDoe",
            password="",
        )

        response = auth_client.authenticate(credentials)

        should_have_status(response, HTTPStatus.BAD_REQUEST)
        should_have_validation_error(
            response,
            field="password",
            message="This field may not be blank.",
        )

    @allure.title("Verify a username is required")
    def test_username_is_required(self, auth_client: AuthClient):
        credentials = AuthFactory.build_missing("username")

        response = auth_client.authenticate_raw(credentials)

        should_have_status(response, HTTPStatus.BAD_REQUEST)
        should_have_validation_error(
            response,
            field="username",
            message="This field is required.",
        )

    @allure.title("Verify a password is required")
    def test_password_is_required(self, auth_client: AuthClient):
        credentials = AuthFactory.build_missing("password")

        response = auth_client.authenticate_raw(credentials)

        should_have_status(response, HTTPStatus.BAD_REQUEST)
        should_have_validation_error(
            response,
            field="password",
            message="This field is required.",
        )
