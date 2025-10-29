"""Support for Liebherr autodoor devices."""

import asyncio
import logging

from homeassistant.components.cover import CoverEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities
):
    """Set up Liebherr covers from a config entry."""
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
            if control["type"] == "autodoor":
                entities.extend(
                    [
                        LiebherrCover(api, coordinator, appliance, control),
                    ]
                )
                # entities.append(LiebherrCover(api, coordinator, appliance, control))

    async_add_entities(entities)


class LiebherrCover(CoverEntity):
    """Representation of a Liebherr cover entity."""

    def __init__(self, api, coordinator, appliance, control) -> None:
        """Initialize the cover entity."""
        self._api = api
        self._coordinator = coordinator
        self._appliance = appliance
        self._control = control
        self._identifier = control.get("identifier", control["type"])
        self._attr_name = f"{appliance['nickname']} {self._identifier}"
        self._attr_unique_id = f"{appliance['deviceId']}_{self._identifier}"
        self._is_opening = False
        self._attr_is_closed = not self.is_open

    @property
    def device_info(self):
        """Return device information for the cover."""
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
    def is_open(self):
        """Return true if the cover is open."""
        if not self._coordinator.data:
            _LOGGER.error("Coordinator data is empty")
            return False

        controls = []
        appliances = self._coordinator.data.get("appliances", [])
        for device in appliances:
            if device.get("deviceId") == self._appliance["deviceId"]:
                controls = device.get("controls", [])
                for control in controls:
                    if control.get("identifier", control["type"]) == self._identifier:
                        return control.get("active", False)
        return False

    @property
    def available(self):
        """Return True if the cover is available."""
        return True

    async def async_open_cover(self, **kwargs):
        """Open the cover."""
        if self._control["type"] == "autodoor":
            await self._api.set_value(
                self._appliance["deviceId"] + "/" + self._control["endpoint"],
                {"autoDoorMode": "OPEN"},
            )
        self._is_opening = True
        await asyncio.sleep(5)
        self._is_opening = False
        await self._coordinator.async_request_refresh()

    @property
    def is_opening(self):
        """Return if the cover is opening or not."""
        return self._is_opening

    async def async_close_cover(self, **kwargs):
        """Close the cover."""
        # Closing is automatic, no action needed
