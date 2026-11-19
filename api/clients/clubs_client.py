import allure
from requests import Response

from api.clients.http_client import HTTPClient
from api.models.requests.create_club_request import CreateClubRequest
from api.models.requests.patch_club_request import PatchClubRequest
from utils.routes import APIRoutes


class ClubsClient(HTTPClient):
    @allure.step("Create club")
    def create_club(self, club: CreateClubRequest) -> Response:
        return self.post(APIRoutes.CLUBS, club)

    @allure.step("Create club using raw payload")
    def create_club_raw(self, payload: dict) -> Response:
        return self.post_raw(APIRoutes.CLUBS, payload)

    @allure.step("Get club with id '{club_id}'")
    def get_club(self, club_id: int) -> Response:
        return self.get(APIRoutes.CLUB_DETAILS.format(club_id=club_id))

    @allure.step("Update club with id '{club_id}'")
    def patch_club(self, club_id: int, payload: PatchClubRequest) -> Response:
        return self.patch(APIRoutes.CLUB_DETAILS.format(club_id=club_id), payload)

    @allure.step("Update club using raw payload")
    def patch_club_raw(self, club_id: int, payload: dict) -> Response:
        return self.patch_raw(APIRoutes.CLUB_DETAILS.format(club_id=club_id), payload)

    @allure.step("Delete club with id '{club_id}'")
    def delete_club(self, club_id: int) -> Response:
        return self.delete(APIRoutes.CLUB_DETAILS.format(club_id=club_id))
