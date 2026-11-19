from api.models.base import ApiModel


class CreateClubRequest(ApiModel):
    book_title: str | None = None
    book_authors: str | None = None
    publication_year: int | None = None
    description: str | None = None
    telegram_chat_link: str | None = None
