from http import HTTPStatus

import allure
import pytest
from allure_commons.types import Severity

from api.clients.clubs_client import ClubsClient
from api.models.requests.patch_club_request import PatchClubRequest
from api.models.responses.club_response import ClubResponse
from assertions.common import should_have_status
from assertions.errors import should_have_validation_error
from factories.club_factory import ClubFactory


@allure.feature("Clubs")
@allure.story("Club Update")
@allure.severity(Severity.CRITICAL)
@pytest.mark.api
class TestEditClub:

    @allure.title("User can update a club")
    def test_update_club_successfully(
        self, authorized_clubs_client: ClubsClient, created_club: ClubResponse
    ):
        patch_payload = PatchClubRequest(description="Updated description")

        response = authorized_clubs_client.patch_club(created_club.id, patch_payload)

        should_have_status(response, HTTPStatus.OK)
        updated_club = ClubResponse.model_validate(response.json())

        assert updated_club.description == "Updated description"
        assert updated_club.id == created_club.id
        assert updated_club.book_title == created_club.book_title
        assert updated_club.book_authors == created_club.book_authors
        assert updated_club.publication_year == created_club.publication_year
        assert updated_club.telegram_chat_link == created_club.telegram_chat_link

    @allure.title("User cannot update an unknown club")
    def test_user_cannot_update_unknown_club(
        self, authorized_clubs_client: ClubsClient
    ):
        non_existent_club_id = 0
        patch_payload = PatchClubRequest(description="Updated description")

        response = authorized_clubs_client.patch_club(
            non_existent_club_id, patch_payload
        )

        should_have_status(response, HTTPStatus.NOT_FOUND)
        should_have_validation_error(
            response,
            field="detail",
            message="No Club matches the given query.",
        )

    @allure.title("Title cannot be blank")
    def test_book_title_cannot_be_blank(
        self, authorized_clubs_client: ClubsClient, created_club: ClubResponse
    ):
        patch_payload = PatchClubRequest(book_title="")

        response = authorized_clubs_client.patch_club(created_club.id, patch_payload)

        should_have_status(response, HTTPStatus.BAD_REQUEST)
        should_have_validation_error(
            response, field="bookTitle", message="This field may not be blank."
        )

    @allure.title("Telegram link should be valid")
    def test_telegram_link_must_be_valid(
        self, authorized_clubs_client: ClubsClient, created_club: ClubResponse
    ):
        patch_payload = PatchClubRequest(telegram_chat_link="test")

        response = authorized_clubs_client.patch_club(created_club.id, patch_payload)

        should_have_status(response, HTTPStatus.BAD_REQUEST)
        should_have_validation_error(
            response, field="telegramChatLink", message="Enter a valid URL."
        )

    @allure.title("Publication year should be a valid year")
    def test_publication_year_must_be_valid(
        self, authorized_clubs_client: ClubsClient, created_club: ClubResponse
    ):
        patch_payload = ClubFactory.build_invalid(publication_year=[])

        response = authorized_clubs_client.patch_club_raw(
            created_club.id, patch_payload
        )

        should_have_status(response, HTTPStatus.BAD_REQUEST)
        should_have_validation_error(
            response, field="publicationYear", message="A valid integer is required."
        )
