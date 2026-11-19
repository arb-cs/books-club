from dataclasses import dataclass

from api.models.requests.register_user_request import RegisterUserRequest
from api.models.responses.auth_user_response import AuthUserResponse
from api.models.responses.user_response import UserResponse


@dataclass
class UserContext:
    registration_request: RegisterUserRequest
    registered_user: UserResponse
    auth: AuthUserResponse | None = None
