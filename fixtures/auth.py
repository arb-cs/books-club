from typing import Any, Generator

import pytest

from api.clients.auth_client import AuthClient
from api.clients.users_client import UsersClient
from api.models.requests.auth_user_request import AuthUserRequest
from api.models.responses.auth_user_response import AuthUserResponse
from fixtures.models import UserContext


@pytest.fixture
def authenticated_user(
    registered_user: UserContext, auth_client: AuthClient
) -> Generator[UserContext, Any, None]:
    auth_request = AuthUserRequest(
        username=registered_user.registration_request.username,
        password=registered_user.registration_request.password,
    )

    auth_response = auth_client.authenticate(auth_request)

    registered_user.auth = AuthUserResponse.model_validate(auth_response.json())

    yield registered_user

    authorized_client = UsersClient(token=registered_user.auth.access)
    authorized_client.delete_current_user()
