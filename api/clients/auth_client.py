import allure
from requests import Response

from api.clients.http_client import HTTPClient
from api.models.requests.auth_user_request import AuthUserRequest
from api.models.requests.refresh_token_request import RefreshTokenRequest
from utils.routes import APIRoutes


class AuthClient(HTTPClient):
    @allure.step("Authenticate user")
    def authenticate(self, login_pair: AuthUserRequest) -> Response:
        return self.post(APIRoutes.AUTH_TOKEN, login_pair)

    def authenticate_raw(self, login_pair: dict) -> Response:
        return self.post_raw(APIRoutes.AUTH_TOKEN, login_pair)

    @allure.step("Refresh access token")
    def refresh_token(self, refresh_token: RefreshTokenRequest) -> Response:
        return self.post(APIRoutes.AUTH_REFRESH, refresh_token)
