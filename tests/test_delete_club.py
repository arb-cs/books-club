from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from api.clients.clubs_client import ClubsClient
from api.models.responses.club_response import ClubResponse
from assertions.common import should_have_status
from assertions.errors import should_have_validation_error


@allure.feature("Clubs")
@allure.story("Club Delete")
@allure.severity(Severity.CRITICAL)
@pytest.mark.api
class TestDeleteClub:
    @allure.title("User can delete club")
    def test_delete_club_successfully(
        self, authorized_clubs_client: ClubsClient, created_club: ClubResponse
    ):
        delete_response = authorized_clubs_client.delete_club(created_club.id)

        should_have_status(
            delete_response,
            HTTPStatus.NO_CONTENT,
        )

        get_response = authorized_clubs_client.get_club(created_club.id)

        should_have_status(get_response, HTTPStatus.NOT_FOUND)

    @allure.title("User get an error when tries to delete unknown club")
    def test_delete_unknown_club(self, authorized_clubs_client: ClubsClient):
        non_existent_club_id = 0
        response = authorized_clubs_client.get_club(non_existent_club_id)

        should_have_status(response, HTTPStatus.NOT_FOUND)
        should_have_validation_error(
            response, field="detail", message="No Club matches the given query."
        )
