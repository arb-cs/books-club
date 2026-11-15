import pytest

from api.clients.users_client import UsersClient
from api.models.responses.user_response import UserResponse
from factories.user_factory import UserFactory
from fixtures.models import UserContext


@pytest.fixture
def registered_user(users_client: UsersClient):
    user = UserFactory.build()

    response = users_client.register_user(user)
    registered_user = UserResponse.model_validate(response.json())

    return UserContext(
        registration_request=user,
        registered_user=registered_user,
    )
