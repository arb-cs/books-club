from datetime import datetime

from api.models.base import ApiModel
from api.models.responses.book_review_response import (
    BookReviewResponse,
)


class ClubResponse(ApiModel):
    id: int
    book_title: str
    book_authors: str
    publication_year: int
    description: str
    telegram_chat_link: str
    owner: int
    members: list[int]
    reviews: list[BookReviewResponse]
    created: datetime
    modified: datetime | None
