from api.models.base import ApiModel


class RegisterUserRequest(ApiModel):
    username: str
    password: str
