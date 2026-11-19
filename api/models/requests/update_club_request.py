from pydantic import HttpUrl

from api.models.base import ApiModel


class UpdateClubRequest(ApiModel):
    book_title: str
    book_authors: str
    publication_year: int
    description: str
    telegram_chat_link: HttpUrl
