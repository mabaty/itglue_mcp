import asyncio
import os
from typing import Any

import httpx

_REGION_URLS = {
    "us": "https://api.itglue.com",
    "eu": "https://api.eu.itglue.com",
    "au": "https://api.au.itglue.com",
}

_RETRY_DELAYS = (2, 4, 8)


class ITGlueError(Exception):
    def __init__(self, status: int, body: str) -> None:
        self.status = status
        super().__init__(f"IT Glue API error {status}: {body}")


class ITGlueClient:
    def __init__(self) -> None:
        api_key = os.environ.get("ITGLUE_API_KEY")
        if not api_key:
            raise RuntimeError("ITGLUE_API_KEY environment variable is required")
        region = os.environ.get("ITGLUE_REGION", "us").lower()
        base_url = _REGION_URLS.get(region)
        if not base_url:
            raise RuntimeError(f"Unknown ITGLUE_REGION '{region}'. Use: us, eu, au")
        self._http = httpx.AsyncClient(
            base_url=base_url,
            headers={
                "x-api-key": api_key,
                "Content-Type": "application/vnd.api+json",
                "Accept": "application/vnd.api+json",
            },
            timeout=30.0,
        )

    async def _request(self, method: str, path: str, **kwargs: Any) -> Any:
        for attempt, delay in enumerate((*_RETRY_DELAYS, None)):
            response = await self._http.request(method, path, **kwargs)
            if response.status_code == 429 and delay is not None:
                await asyncio.sleep(delay)
                continue
            if response.status_code >= 400:
                raise ITGlueError(response.status_code, response.text)
            if response.status_code == 204:
                return None
            return response.json()

    async def get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        return await self._request("GET", path, params=params)

    async def post(self, path: str, data: dict[str, Any]) -> Any:
        return await self._request("POST", path, json=data)

    async def patch(self, path: str, data: dict[str, Any]) -> Any:
        return await self._request("PATCH", path, json=data)

    async def delete(self, path: str) -> None:
        await self._request("DELETE", path)

    async def aclose(self) -> None:
        await self._http.aclose()


def unwrap(response: Any) -> Any:
    """Flatten JSON:API envelope to plain dicts."""
    if isinstance(response, dict):
        data = response.get("data")
        meta = response.get("meta")
        if data is None:
            return response
        flat = _flatten(data)
        if meta:
            return {"data": flat, "meta": meta}
        return flat
    return response


def _flatten(data: Any) -> Any:
    if isinstance(data, list):
        return [_flatten(item) for item in data]
    if isinstance(data, dict) and "id" in data and "attributes" in data:
        result = {"id": data["id"], "type": data.get("type")}
        result.update(data["attributes"])
        return result
    return data
