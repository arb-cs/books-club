from api.models.base import ApiModel


class AuthUserResponse(ApiModel):
    refresh: str
    access: str
