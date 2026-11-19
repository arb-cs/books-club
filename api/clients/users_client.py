import allure
from requests import Response

from api.clients.http_client import HTTPClient
from api.models.requests.register_user_request import RegisterUserRequest
from utils.routes import APIRoutes


class UsersClient(HTTPClient):
    @allure.step("Register a new user")
    def register_user(self, user: RegisterUserRequest) -> Response:
        return self.post(APIRoutes.REGISTER, user)

    @allure.step("Register user using raw payload")
    def register_user_raw(self, payload: dict) -> Response:
        return self.post_raw(APIRoutes.REGISTER, payload)

    @allure.step("Get user")
    def get_user(self) -> Response:
        return self.get(APIRoutes.USER_ME)

    @allure.step("Delete a user")
    def delete_current_user(self):
        return self.delete(APIRoutes.USER_ME)
