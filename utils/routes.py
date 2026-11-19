from enum import StrEnum


class APIRoutes(StrEnum):
    REGISTER = "/api/v1/users/register/"
    USER_ME = "/api/v1/users/me"

    AUTH_TOKEN = "/api/v1/auth/token/"
    AUTH_REFRESH = "/api/v1/auth/token/refresh/"

    CLUBS = "/api/v1/clubs/"
    CLUB_DETAILS = "/api/v1/clubs/{club_id}/"
