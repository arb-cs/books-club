from api.models.base import ApiModel


class AuthUserRequest(ApiModel):
    username: str
    password: str
