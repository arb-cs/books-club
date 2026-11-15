from api.models.base import ApiModel


class UserResponse(ApiModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    remote_addr: str
