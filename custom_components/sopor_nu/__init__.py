"""The Sopor.nu integration."""

from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_MUNICIPALITY_CODE, CONF_STATION_ID, CONF_STATION_NAME, DOMAIN
from .coordinator import SoporNuCoordinator

PLATFORMS = [Platform.SENSOR]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Sopor.nu from a config entry."""
    coordinator = SoporNuCoordinator(
        hass,
        station_id=entry.data[CONF_STATION_ID],
        municipality_code=entry.data[CONF_MUNICIPALITY_CODE],
        station_name=entry.data[CONF_STATION_NAME],
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    if unload_ok := await hass.config_entries.async_unload_platforms(
        entry, PLATFORMS
    ):
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok
