from faker import Faker

from api.models.requests.auth_user_request import AuthUserRequest
from api.models.requests.refresh_token_request import RefreshTokenRequest

fake = Faker()


class AuthFactory:
    @staticmethod
    def build(username: str, password: str) -> AuthUserRequest:
        return AuthUserRequest(
            username=username,
            password=password,
        )

    @staticmethod
    def build_missing(field: str) -> dict:
        payload = {
            "username": fake.user_name(),
            "password": fake.password(),
        }

        payload.pop(field)

        return payload

    @staticmethod
    def build_refresh(refresh: str) -> RefreshTokenRequest:
        return RefreshTokenRequest(refresh=refresh)
