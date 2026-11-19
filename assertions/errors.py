import allure
from requests import Response


@allure.step("Verify validation error for field '{field}'")
def should_have_validation_error(
    response: Response,
    field: str,
    message: str,
) -> None:
    errors = response.json()

    assert field in errors
    assert message in errors[field]
