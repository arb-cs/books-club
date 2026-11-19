from api.models.base import ApiModel


class ReviewAuthorResponse(ApiModel):
    id: int
    username: str
