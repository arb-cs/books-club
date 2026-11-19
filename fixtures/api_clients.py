import pytest

from api.clients.auth_client import AuthClient
from api.clients.clubs_client import ClubsClient
from api.clients.users_client import UsersClient
from fixtures.models import UserContext


@pytest.fixture
def users_client() -> UsersClient:
    return UsersClient()


@pytest.fixture
def auth_client() -> AuthClient:
    return AuthClient()


@pytest.fixture
def authorized_users_client(authenticated_user: UserContext) -> UsersClient:
    return UsersClient(token=authenticated_user.auth.access)


@pytest.fixture
def authorized_clubs_client(authenticated_user: UserContext) -> ClubsClient:
    return ClubsClient(
        token=authenticated_user.auth.access,
    )
