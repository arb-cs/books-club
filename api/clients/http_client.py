import json

import requests
from pydantic import BaseModel
from requests import Response

from api.config.settings import settings
from utils.http_method import HTTPMethod
from utils.logger import logger


class HTTPClient:
    def __init__(self, token: str | None = None):
        self.session = requests.Session()
        self.base_url = settings.base_url

        self.session.headers.update(
            {
                "Content-Type": "application/json",
            }
        )

        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def _request(self, method: HTTPMethod, endpoint: str, **kwargs) -> Response:
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(
                method=method, url=url, timeout=settings.request_timeout, **kwargs
            )

            json_payload = kwargs.get("json")

            if response.status_code >= 400:
                logger.error(
                    "%s %s -> %s\nPayload:\n%s\nResponse:\n%s",
                    method,
                    endpoint,
                    response.status_code,
                    json.dumps(json_payload, indent=2) if json_payload else "None",
                    response.text,
                )
            else:
                logger.info("%s %s -> %s", method, endpoint, response.status_code)

            return response

        except requests.RequestException:
            logger.exception("%s %s failed", method, url)
            raise

    def get(self, endpoint: str, **kwargs) -> Response:
        return self._request(HTTPMethod.GET, endpoint, **kwargs)

    def post(self, endpoint: str, payload: BaseModel) -> Response:
        return self._request(
            HTTPMethod.POST,
            endpoint,
            json=payload.model_dump(by_alias=True, exclude_none=True),
        )

    def post_raw(self, endpoint: str, payload: dict) -> Response:
        return self._request(HTTPMethod.POST, endpoint, json=payload)

    def put(self, endpoint: str, payload: BaseModel) -> Response:
        return self._request(
            HTTPMethod.PUT, endpoint, json=payload.model_dump(by_alias=True)
        )

    def patch(self, endpoint: str, payload: BaseModel) -> Response:
        return self._request(
            HTTPMethod.PATCH,
            endpoint,
            json=payload.model_dump(by_alias=True, exclude_none=True),
        )

    def patch_raw(self, endpoint: str, payload: dict) -> Response:
        return self._request(HTTPMethod.PATCH, endpoint, json=payload)

    def delete(self, endpoint: str) -> Response:
        return self._request(HTTPMethod.DELETE, endpoint)
