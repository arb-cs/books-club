from faker import Faker

from api.models.requests.create_club_request import CreateClubRequest

fake = Faker()


class ClubFactory:

    @staticmethod
    def build(**overrides) -> CreateClubRequest:
        data = {
            "book_title": fake.sentence(nb_words=3).rstrip("."),
            "book_authors": fake.name(),
            "publication_year": fake.year(),
            "description": fake.paragraph(nb_sentences=5),
            "telegram_chat_link": f"https://t.me/{fake.user_name()}",
        }

        data.update(overrides)

        return CreateClubRequest(**data)

    @staticmethod
    def build_invalid(**overrides) -> dict:
        data = {
            "book_title": fake.sentence(nb_words=3).rstrip("."),
            "book_authors": fake.name(),
            "publication_year": int(fake.year()),
            "description": fake.paragraph(nb_sentences=5),
            "telegram_chat_link": f"https://t.me/{fake.user_name()}",
        }

        data.update(overrides)

        return data

    @staticmethod
    def build_missing(field: str):
        data = {
            "book_title": fake.sentence(nb_words=3).rstrip("."),
            "book_authors": fake.name(),
            "publication_year": int(fake.year()),
            "description": fake.paragraph(nb_sentences=5),
            "telegram_chat_link": f"https://t.me/{fake.user_name()}",
        }

        data.pop(field)

        return data
