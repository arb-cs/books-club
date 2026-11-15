from faker import Faker

from api.models.requests.register_user_request import RegisterUserRequest

fake = Faker()


class UserFactory:
    @staticmethod
    def build(**overrides) -> RegisterUserRequest:
        payload = {
            "username": fake.user_name(),
            "password": fake.password(length=12),
        }

        payload.update(overrides)

        return RegisterUserRequest(**payload)

    @staticmethod
    def build_invalid(**overrides) -> dict:
        payload = {
            "username": fake.user_name(),
            "password": fake.password(length=12),
        }

        payload.update(overrides)

        return payload

    @staticmethod
    def build_missing(field: str) -> dict:
        payload = {
            "username": fake.user_name(),
            "password": fake.password(),
        }

        payload.pop(field)

        return payload
