from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from api.clients.clubs_client import ClubsClient
from api.models.responses.club_response import ClubResponse
from assertions.common import should_have_status
from assertions.errors import should_have_validation_error


@allure.feature("Clubs")
@allure.story("Club Get")
@allure.severity(Severity.CRITICAL)
@pytest.mark.api
class TestGetClub:
    @allure.title("User can get created club")
    def test_get_club_successfully(
        self, authorized_clubs_client: ClubsClient, created_club: ClubResponse
    ):
        response = authorized_clubs_client.get_club(created_club.id)

        should_have_status(response, HTTPStatus.OK)
        club = ClubResponse.model_validate(response.json())

        assert club.id == created_club.id
        assert club.book_title == created_club.book_title

    @allure.title("User get an error when they try to get unknown club")
    def test_get_unknown_club(self, authorized_clubs_client: ClubsClient):
        response = authorized_clubs_client.get_club(0)

        should_have_status(response, HTTPStatus.NOT_FOUND)
        should_have_validation_error(
            response, field="detail", message="No Club matches the given query."
        )
