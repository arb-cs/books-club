from api.models.base import ApiModel


class RefreshTokenRequest(ApiModel):
    refresh: str
