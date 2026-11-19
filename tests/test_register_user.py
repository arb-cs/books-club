from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from api.clients.users_client import UsersClient
from api.models.responses.user_response import UserResponse
from assertions.common import should_have_status
from assertions.errors import should_have_validation_error
from assertions.users import assert_registered_user
from factories.user_factory import UserFactory
from fixtures.models import UserContext


@allure.feature("Registration")
@allure.story("User Registration")
@allure.severity(Severity.CRITICAL)
@pytest.mark.api
@pytest.mark.registration
class TestUserRegistration:

    @allure.title("Register user")
    def test_register_user_successfully(self, users_client: UsersClient):
        payload = UserFactory.build()

        response = users_client.register_user(payload)

        should_have_status(response, HTTPStatus.CREATED)
        registered_user = UserResponse.model_validate(response.json())
        assert_registered_user(request=payload, response=registered_user)

    @allure.title("User cannot be registered twice")
    def test_register_user_fails_if_user_already_exists(
        self,
        authenticated_user: UserContext,
        users_client: UsersClient,
    ):
        payload = UserFactory.build(
            username=authenticated_user.registration_request.username,
            password=authenticated_user.registration_request.password,
        )

        response = users_client.register_user(payload)

        should_have_status(response, HTTPStatus.BAD_REQUEST)
        should_have_validation_error(
            response,
            field="username",
            message="A user with that username already exists.",
        )

    @allure.title("Username cannot be blank")
    def test_username_cannot_be_blank(self, users_client: UsersClient):
        payload = UserFactory.build(username="")

        response = users_client.register_user(payload)

        should_have_status(response, HTTPStatus.BAD_REQUEST)
        should_have_validation_error(
            response, field="username", message="This field may not be blank."
        )

    @allure.title("Password cannot be blank")
    def test_password_cannot_be_blank(self, users_client: UsersClient):
        payload = UserFactory.build(password="")

        response = users_client.register_user(payload)

        should_have_status(response, HTTPStatus.BAD_REQUEST)
        should_have_validation_error(
            response, field="password", message="This field may not be blank."
        )

    @allure.title("Username cannot have an incorrect type")
    def test_username_cannot_have_invalid_type(self, users_client: UsersClient):
        payload = UserFactory.build_invalid(username=True)

        response = users_client.register_user_raw(payload)

        should_have_status(response, HTTPStatus.BAD_REQUEST)
        should_have_validation_error(
            response, field="username", message="Not a valid string."
        )

    @allure.title("Password cannot have incorrect type")
    def test_password_cannot_have_invalid_type(self, users_client: UsersClient):
        payload = UserFactory.build_invalid(password={})

        response = users_client.register_user_raw(payload)

        should_have_status(response, HTTPStatus.BAD_REQUEST)
        should_have_validation_error(
            response, field="password", message="Not a valid string."
        )

    @allure.title("Username is required")
    def test_username_is_required(self, users_client: UsersClient):
        payload = UserFactory.build_missing("username")

        response = users_client.register_user_raw(payload)

        should_have_status(response, HTTPStatus.BAD_REQUEST)
        should_have_validation_error(
            response, field="username", message="This field is required."
        )

    @allure.title("Password is required")
    def test_password_is_required(self, users_client: UsersClient):
        payload = UserFactory.build_missing("password")

        response = users_client.register_user_raw(payload)

        should_have_status(response, HTTPStatus.BAD_REQUEST)
        should_have_validation_error(
            response, field="password", message="This field is required."
        )

    @allure.title("Username cannot be longer than 150 characters")
    def test_username_cannot_exceed_150_characters(self, users_client: UsersClient):
        payload = UserFactory.build_invalid(username="A" * 151)

        response = users_client.register_user_raw(payload)

        should_have_status(response, HTTPStatus.BAD_REQUEST)
        should_have_validation_error(
            response,
            field="username",
            message="Ensure this field has no more than 150 characters.",
        )

    @allure.title("Password cannot be longer than 128 characters")
    def test_password_cannot_exceed_128_characters(self, users_client: UsersClient):
        payload = UserFactory.build_invalid(password="A" * 129)

        response = users_client.register_user_raw(payload)

        should_have_status(response, HTTPStatus.BAD_REQUEST)
        should_have_validation_error(
            response,
            field="password",
            message="Ensure this field has no more than 128 characters.",
        )
