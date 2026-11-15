import pytest

from api.clients.clubs_client import ClubsClient
from api.models.responses.club_response import ClubResponse
from factories.club_factory import ClubFactory


@pytest.fixture
def created_club(authorized_clubs_client: ClubsClient) -> ClubResponse:
    payload = ClubFactory.build()

    response = authorized_clubs_client.create_club(payload)
    club = ClubResponse.model_validate(response.json())

    yield club

    get_response = authorized_clubs_client.get_club(club.id)

    if get_response.status_code == 200:
        authorized_clubs_client.delete_club(club.id)
