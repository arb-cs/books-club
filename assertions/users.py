import allure

from api.models.requests.register_user_request import RegisterUserRequest
from api.models.responses.user_response import UserResponse


@allure.step("Verify user was registered successfully")
def assert_registered_user(
    request: RegisterUserRequest,
    response: UserResponse,
) -> None:
    assert response.username == request.username

    assert response.first_name == "", "An empty first_name field is required."
    assert response.last_name == "", "An empty last_name field is required."
    assert response.email == "", "An empty email field is required."

    assert response.remote_addr, "A remote address field is required."
