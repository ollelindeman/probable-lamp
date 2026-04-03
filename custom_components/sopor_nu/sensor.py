"""Sensor platform for the Sopor.nu integration."""

from __future__ import annotations

from datetime import datetime
import logging
from typing import Any

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
    CONF_MUNICIPALITY_CODE,
    CONF_STATION_ID,
    CONF_STATION_NAME,
    DOMAIN,
    SERVICE_TYPE_ICONS,
    SERVICE_TYPE_NAMES,
    SERVICE_TYPE_NAMES_SV,
)
from .coordinator import SoporNuCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Sopor.nu sensors from a config entry."""
    coordinator: SoporNuCoordinator = hass.data[DOMAIN][entry.entry_id]

    entities: list[SoporNuServiceSensor] = []
    services = coordinator.data.get("services", {})

    for service_type, service_data in services.items():
        entities.append(
            SoporNuServiceSensor(coordinator, entry, service_type, service_data)
        )

    async_add_entities(entities)


class SoporNuServiceSensor(
    CoordinatorEntity[SoporNuCoordinator], SensorEntity
):
    """Sensor for a recycling station service (trash type)."""

    _attr_has_entity_name = True
    _attr_device_class = SensorDeviceClass.TIMESTAMP

    def __init__(
        self,
        coordinator: SoporNuCoordinator,
        entry: ConfigEntry,
        service_type: int,
        service_data: dict[str, Any],
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)

        station_id = entry.data[CONF_STATION_ID]
        station_name = entry.data[CONF_STATION_NAME]
        municipality_code = entry.data[CONF_MUNICIPALITY_CODE]

        self._service_type = service_type
        self._attr_unique_id = f"{municipality_code}_{station_id}_{service_type}"
        self._attr_translation_key = f"service_{service_type}"

        type_name = SERVICE_TYPE_NAMES.get(service_type, f"Unknown ({service_type})")
        self._attr_name = type_name
        self._attr_icon = SERVICE_TYPE_ICONS.get(service_type, "mdi:recycle")

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, f"{municipality_code}_{station_id}")},
            name=station_name,
            manufacturer="Avfall Sverige",
            model="Recycling Station",
            entry_type=DeviceEntryType.SERVICE,
            configuration_url=f"https://www.sopor.nu/haer-aatervinner-du/hitta-aatervinningen/?avs={station_id}&kommun={municipality_code}",
        )

    @property
    def native_value(self) -> datetime | None:
        """Return the last action date as the sensor state."""
        service = self.coordinator.data.get("services", {}).get(
            self._service_type
        )
        if not service:
            return None

        last_action = service.get("lastAction")
        if last_action:
            return datetime.fromisoformat(last_action)
        return None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return extra state attributes."""
        service = self.coordinator.data.get("services", {}).get(
            self._service_type
        )
        if not service:
            return {}

        attrs: dict[str, Any] = {}

        last_action = service.get("lastAction")
        if last_action:
            attrs["last_action"] = last_action

        next_action = service.get("nextAction")
        if next_action:
            attrs["next_action"] = next_action

        last_alt = service.get("lastActionAltText", "")
        if last_alt:
            attrs["last_action_alt_text"] = last_alt

        next_alt = service.get("nextActionAltText", "")
        if next_alt:
            attrs["next_action_alt_text"] = next_alt

        extra_info = service.get("extraInfo", "")
        if extra_info:
            attrs["extra_info"] = extra_info

        responsible = service.get("responsible", "")
        if responsible:
            attrs["responsible"] = responsible

        sv_name = SERVICE_TYPE_NAMES_SV.get(self._service_type)
        if sv_name:
            attrs["service_name_sv"] = sv_name

        attrs["service_type"] = self._service_type
        attrs["number_of_containers"] = service.get("numberOfServices", 0)

        return attrs
