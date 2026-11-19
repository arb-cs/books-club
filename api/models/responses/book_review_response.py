from datetime import datetime

from api.models.base import ApiModel
from api.models.responses.review_author_response import (
    ReviewAuthorResponse,
)


class BookReviewResponse(ApiModel):
    id: int
    club: int
    user: ReviewAuthorResponse
    review: str
    assessment: int
    read_pages: int
    created: datetime
    modified: datetime | None
