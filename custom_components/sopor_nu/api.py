"""API client for the Sopor.nu (Avfallshubben) API."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp

from .const import API_BASE_URL

_LOGGER = logging.getLogger(__name__)


class SoporNuApiError(Exception):
    """Base exception for Sopor.nu API errors."""


class SoporNuConnectionError(SoporNuApiError):
    """Exception for connection errors."""


class SoporNuApiClient:
    """Async API client for the Avfallshubben Sopor API."""

    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Initialize the API client."""
        self._session = session

    async def get_all_stations(self) -> list[dict[str, Any]]:
        """Fetch the list of all recycling stations."""
        return await self._request("GetAllAVS")

    async def get_station(
        self, station_id: str, municipality_code: str
    ) -> dict[str, Any]:
        """Fetch details for a specific recycling station."""
        params = {
            "externalAvsId": station_id,
            "municipalityCode": municipality_code,
        }
        return await self._request("GetAVS", params=params)

    async def _request(
        self, endpoint: str, params: dict[str, str] | None = None
    ) -> Any:
        """Make an API request."""
        url = f"{API_BASE_URL}{endpoint}"
        try:
            async with asyncio.timeout(30):
                async with self._session.get(url, params=params) as resp:
                    if resp.status != 200:
                        raise SoporNuApiError(
                            f"API request failed with status {resp.status}"
                        )
                    return await resp.json()
        except asyncio.TimeoutError as err:
            raise SoporNuConnectionError("Timeout connecting to API") from err
        except aiohttp.ClientError as err:
            raise SoporNuConnectionError(
                f"Error connecting to API: {err}"
            ) from err
