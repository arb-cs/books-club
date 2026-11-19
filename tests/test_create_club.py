from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from api.clients.clubs_client import ClubsClient
from api.models.responses.club_response import ClubResponse
from assertions.clubs import assert_created_club
from assertions.common import should_have_status
from assertions.errors import should_have_validation_error
from factories.club_factory import ClubFactory


@allure.feature("Clubs")
@allure.story("Club Create")
@allure.severity(Severity.CRITICAL)
@pytest.mark.api
class TestCreateClub:
    @allure.title("User can create a club")
    def test_create_club_successfully(self, authorized_clubs_client: ClubsClient):
        club = ClubFactory.build()

        response = authorized_clubs_client.create_club(club)

        should_have_status(response, HTTPStatus.CREATED)
        created_club = ClubResponse.model_validate(response.json())
        assert_created_club(club, created_club)

    @allure.title("User cannot create a club with the same title twice")
    def test_club_create_fails_if_club_with_that_title_exists(
        self, authorized_clubs_client: ClubsClient, created_club: ClubResponse
    ):
        payload = ClubFactory.build(book_title=created_club.book_title)

        response = authorized_clubs_client.create_club(payload)

        should_have_status(
            response,
            HTTPStatus.BAD_REQUEST,
        )
        should_have_validation_error(
            response,
            field="bookTitle",
            message="Book Club with this Book Title already exists.",
        )

    @allure.title("User cannot create a club when a title has a wrong data type")
    def test_cannot_create_club_with_incorrect_title(
        self, authorized_clubs_client: ClubsClient
    ):
        club = ClubFactory.build_invalid(book_title=True)

        response = authorized_clubs_client.create_club_raw(club)

        should_have_status(response, HTTPStatus.BAD_REQUEST)
        should_have_validation_error(
            response, field="bookTitle", message="Not a valid string."
        )

    @allure.title("User cannot create a club when a title is missing")
    def test_cannot_create_club_with_missing_title(
        self, authorized_clubs_client: ClubsClient
    ):
        club = ClubFactory.build_missing("book_title")

        response = authorized_clubs_client.create_club_raw(club)

        should_have_status(response, HTTPStatus.BAD_REQUEST)
        should_have_validation_error(
            response, field="bookTitle", message="This field is required."
        )
