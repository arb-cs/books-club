import allure

from api.models.requests.create_club_request import CreateClubRequest
from api.models.responses.club_response import ClubResponse


@allure.step("Verify that a club was successfully created")
def assert_created_club(request: CreateClubRequest, response: ClubResponse) -> None:
    assert request.book_title == response.book_title
    assert request.book_authors == response.book_authors
    assert request.publication_year == response.publication_year
    assert request.description == response.description
    assert request.telegram_chat_link == response.telegram_chat_link

    assert response.id
    assert response.owner
    assert response.created
