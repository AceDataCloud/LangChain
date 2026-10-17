"""Shared authenticated HTTP boundary. No automatic retries or background polling."""

import os
from typing import Any

import httpx
from pydantic import SecretStr


class AceAPIClient:
    """HTTP client whose credential is excluded from tool schemas and representations."""

    def __init__(
        self,
        api_token: str | SecretStr | None = None,
        *,
        http_client: httpx.Client | None = None,
        http_async_client: httpx.AsyncClient | None = None,
    ):
        value = api_token or os.environ.get("ACEDATACLOUD_API_TOKEN")
        if not value:
            raise ValueError("Set ACEDATACLOUD_API_TOKEN to an application API Key.")
        self._token = value if isinstance(value, SecretStr) else SecretStr(value)
        self._http = http_client
        self._async_http = http_async_client

    def __repr__(self) -> str:
        return "AceAPIClient(api_token=SecretStr('**********'))"

    def _headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._token.get_secret_value()}",
            "Content-Type": "application/json",
        }

    @staticmethod
    def _url(path: str) -> str:
        # Only fixed service endpoint paths supplied by tool classes are accepted.
        if not path.startswith("/") or path.startswith("//") or "?" in path or "#" in path:
            raise ValueError("Expected a fixed service API path.")
        return "https://api.acedata.cloud" + path

    def post(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        if self._http is not None:
            response = self._http.post(self._url(path), json=body, headers=self._headers())
        else:
            with httpx.Client(timeout=60, follow_redirects=False) as client:
                response = client.post(self._url(path), json=body, headers=self._headers())
        return self._decode(response)

    async def apost(self, path: str, body: dict[str, Any]) -> dict[str, Any]:
        if self._async_http is not None:
            response = await self._async_http.post(
                self._url(path), json=body, headers=self._headers()
            )
        else:
            async with httpx.AsyncClient(timeout=60, follow_redirects=False) as client:
                response = await client.post(self._url(path), json=body, headers=self._headers())
        return self._decode(response)

    @staticmethod
    def _decode(response: httpx.Response) -> dict[str, Any]:
        # Preserve HTTP status/type. The caller decides whether to retry after
        # checking usage; an uncertain generation is never automatically resubmitted.
        response.raise_for_status()
        data = response.json()
        if not isinstance(data, dict):
            raise ValueError("Expected an object from the Ace API.")
        return data
