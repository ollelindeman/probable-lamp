"""DataUpdateCoordinator for the Sopor.nu integration."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import SoporNuApiClient, SoporNuApiError
from .const import DEFAULT_SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)


class SoporNuCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator to fetch data from the Sopor.nu API."""

    def __init__(
        self,
        hass: HomeAssistant,
        station_id: str,
        municipality_code: str,
        station_name: str,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"Sopor.nu {station_name}",
            update_interval=timedelta(seconds=DEFAULT_SCAN_INTERVAL),
        )
        self.station_id = station_id
        self.municipality_code = municipality_code
        self.station_name = station_name
        self._api = SoporNuApiClient(async_get_clientsession(hass))

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch station data from the API."""
        try:
            data = await self._api.get_station(
                self.station_id, self.municipality_code
            )
        except SoporNuApiError as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err

        avs = data.get("avs", {})
        services = avs.get("services", [])

        return {
            "station_id": self.station_id,
            "station_name": self.station_name,
            "municipality_code": self.municipality_code,
            "services": {
                svc["serviceType"]: svc for svc in services
            },
        }
