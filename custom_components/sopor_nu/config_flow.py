"""Config flow for the Sopor.nu integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import SoporNuApiClient, SoporNuApiError
from .const import (
    CONF_MUNICIPALITY_CODE,
    CONF_STATION_ID,
    CONF_STATION_NAME,
    DOMAIN,
    MUNICIPALITIES,
)

_LOGGER = logging.getLogger(__name__)


class SoporNuConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Sopor.nu."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize the config flow."""
        self._all_stations: list[dict[str, Any]] = []
        self._municipality_code: str = ""
        self._municipality_stations: list[dict[str, Any]] = []

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the municipality selection step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            self._municipality_code = user_input[CONF_MUNICIPALITY_CODE]
            api = SoporNuApiClient(async_get_clientsession(self.hass))

            try:
                self._all_stations = await api.get_all_stations()
            except SoporNuApiError:
                errors["base"] = "cannot_connect"
            else:
                self._municipality_stations = sorted(
                    [
                        s
                        for s in self._all_stations
                        if s.get("municipalityCode") == self._municipality_code
                    ],
                    key=lambda s: s.get("name", ""),
                )

                if not self._municipality_stations:
                    errors[CONF_MUNICIPALITY_CODE] = "no_stations"
                else:
                    return await self.async_step_station()

        # Build municipality options: only show municipalities that exist
        # in the API, sorted by name
        available_codes: set[str] = set()
        if self._all_stations:
            available_codes = {
                s.get("municipalityCode", "")
                for s in self._all_stations
            }

        # If we haven't fetched stations yet, show all municipalities
        if available_codes:
            municipality_options = {
                code: f"{MUNICIPALITIES.get(code, code)} ({code})"
                for code in sorted(
                    available_codes,
                    key=lambda c: MUNICIPALITIES.get(c, c),
                )
            }
        else:
            municipality_options = {
                code: f"{name} ({code})"
                for code, name in sorted(
                    MUNICIPALITIES.items(), key=lambda x: x[1]
                )
            }

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_MUNICIPALITY_CODE): vol.In(
                        municipality_options
                    ),
                }
            ),
            errors=errors,
        )

    async def async_step_station(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the station selection step."""
        if user_input is not None:
            station_id = user_input[CONF_STATION_ID]

            station = next(
                (
                    s
                    for s in self._municipality_stations
                    if str(s["externalAvsId"]) == station_id
                ),
                None,
            )

            if station is None:
                return self.async_abort(reason="station_not_found")

            station_name = station.get("name", station_id)

            await self.async_set_unique_id(
                f"{self._municipality_code}_{station_id}"
            )
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=station_name,
                data={
                    CONF_STATION_ID: station_id,
                    CONF_MUNICIPALITY_CODE: self._municipality_code,
                    CONF_STATION_NAME: station_name,
                },
            )

        station_options = {
            str(s["externalAvsId"]): f"{s.get('name', '')} ({s.get('streetAddress', '')})"
            for s in self._municipality_stations
        }

        return self.async_show_form(
            step_id="station",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_STATION_ID): vol.In(station_options),
                }
            ),
        )
