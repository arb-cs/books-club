from http import HTTPStatus

import allure
from requests import Response


@allure.step("Verify response has status code '{expected}'")
def should_have_status(response: Response, expected: HTTPStatus) -> None:
    assert response.status_code == expected, (
        f"\nExpected: {expected.value} {expected.phrase}"
        f"\nActual: {response.status_code}"
        f"\nResponse body:\n{response.text}"
    )
