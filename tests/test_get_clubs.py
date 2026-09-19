import allure
import requests
from jsonschema import validate

from utils.schema_loader import load_schema

BASE_URL = "https://book-club.qa.guru"


@allure.feature("GET method /api/v1/clubs/")
@allure.severity(allure.severity_level.BLOCKER)
@allure.description("Find the club by its name and check that we have found the correct one.")
def test_get_club_by_search():
    response = requests.get(BASE_URL + "/api/v1/clubs/?search=1984")

    body = response.json()
    schema = load_schema("get_club_by_search.json")
    title = body["results"][0]["bookTitle"]
    author = body["results"][0]["bookAuthors"].strip()

    validate(instance=body, schema=schema)
    assert response.status_code == 200
    assert title == "1984"
    assert author == "George Orwell"


@allure.feature("GET method /api/v1/clubs/")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("Checking a response regarding a non-existent club.")
def test_get_club_by_search_unknown_info():
    response = requests.get(BASE_URL + "/api/v1/clubs/?search=unknown_info")

    body = response.json()
    schema = load_schema("empty_results.json")
    count = body["count"]
    results = body["results"]

    validate(instance=body, schema=schema)
    assert response.status_code == 200
    assert count == 0
    assert results == []


@allure.feature("GET method /api/v1/clubs/")
@allure.severity(allure.severity_level.NORMAL)
@allure.description("Checking a response regarding a non-existent club.")
def test_get_clubs_invalid_page():
    response = requests.get(BASE_URL + "/api/v1/clubs/?page=-50")

    body = response.json()
    detail = body["detail"]

    assert response.status_code == 404
    assert detail == "Invalid page."
