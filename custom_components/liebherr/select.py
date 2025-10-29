"""Support for Liebherr mode selections."""

import asyncio
import logging

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .models import ModeControlRequest

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities
):
    """Set up Liebherr selects from a config entry."""
    api = hass.data[DOMAIN][config_entry.entry_id]["api"]
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    appliances = await api.get_appliances()

    entities = []
    for appliance in appliances:
        controls = await api.get_controls(appliance["deviceId"])
        if not controls:
            _LOGGER.warning("No controls found for appliance %s",
                            appliance["deviceId"])
            continue

        for control in controls:
            if control["type"] in ("biofreshplus", "hydrobreeze"):
                entities.extend(
                    [
                        LiebherrSelect(api, coordinator, appliance, control),
                    ]
                )

    async_add_entities(entities)


class LiebherrSelect(SelectEntity):
    """Representation of a Liebherr select entity."""

    def __init__(self, api, coordinator, appliance, control) -> None:
        """Initialize the select entity."""
        self._api = api
        self._coordinator = coordinator
        self._appliance = appliance
        self._control = control
        self._identifier = control.get("identifier", control["type"])
        self._attr_name = f"{appliance['nickname']} {self._identifier}"
        self._attr_unique_id = f"{appliance['deviceId']}_{self._identifier}"
        self._attr_options = control.get("supportedModes", [])
        match control.get("identifier", control["type"]):
            case "biofreshplus":
                self._attr_icon = "mdi:leaf"
            case "hydrobreeze":
                self._attr_icon = "mdi:water"
                self._attr_options = ["OFF", "LOW", "MEDIUM", "HIGH"]

    @property
    def device_info(self):
        """Return device information for the select."""
        return {
            "identifiers": {(DOMAIN, self._appliance["deviceId"])},
            "name": self._appliance.get(
                "nickname", f"Liebherr HomeAPI Appliance {self._appliance['deviceId']}"
            ),
            "manufacturer": "Liebherr",
            "model": self._appliance.get("model", self._appliance["model"]),
            "sw_version": self._appliance.get("softwareVersion", ""),
        }

    @property
    def current_option(self):
        """Return the current selected option."""
        if not self._coordinator.data:
            _LOGGER.error("Coordinator data is empty")
            return None

        controls = []
        appliances = self._coordinator.data.get("appliances", [])
        for device in appliances:
            if device.get("deviceId") == self._appliance["deviceId"]:
                controls = device.get("controls", [])
                for control in controls:
                    if control.get("identifier", control["type"]) == self._identifier:
                        return control.get("currentMode", None)
        return None

    async def async_select_option(self, option: str):
        """Change the selected option."""
        if option not in self._attr_options:
            _LOGGER.error("Invalid option selected: %s", option)
            return

        data = ModeControlRequest(mode=option)
        await self.api.set_value(
            self._appliance["deviceId"], self._control["name"], data
        )

        await asyncio.sleep(5)
        await self._coordinator.async_request_refresh()
