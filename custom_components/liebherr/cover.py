"""Support for Liebherr autodoor devices."""

import asyncio
import logging
from homeassistant.components.cover import CoverEntity, CoverEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import STATE_OPEN, STATE_CLOSED, STATE_OPENING, STATE_UNKNOWN

from .const import DOMAIN
from .models import AutoDoorControl

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
            _LOGGER.warning("No controls found for appliance %s", appliance["deviceId"])
            continue

        for control in controls:
            if control["type"] == "AutoDoorControl":
                entities.append(LiebherrCover(api, coordinator, appliance, control))

    async_add_entities(entities)


class LiebherrCover(CoverEntity):
    """Representation of a Liebherr auto door cover."""

    def __init__(self, api, coordinator, appliance, control) -> None:
        """Initialize the cover entity."""
        self._api = api
        self._coordinator = coordinator
        self._appliance = appliance
        self._control = control

        self._device_id = appliance["deviceId"]
        self._identifier = control.get("identifier", control["type"])

        self._attr_name = f"{appliance.get('nickname', 'Liebherr')} {self._identifier}"
        self._attr_unique_id = f"{self._device_id}_{self._identifier}"
        self._attr_device_class = "door"
        self._attr_supported_features = CoverEntityFeature.OPEN | CoverEntityFeature.CLOSE

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._appliance.get("nickname", f"Liebherr {self._device_id}"),
            "manufacturer": "Liebherr",
            "model": self._appliance.get("model", ""),
            "sw_version": self._appliance.get("softwareVersion", ""),
        }

    def _get_control_state(self):
        """Return the current state of the control."""
        if not self._coordinator.data:
            return None

        for device in self._coordinator.data.get("appliances", []):
            if device.get("deviceId") != self._device_id:
                continue
            for control in device.get("controls", []):
                if control.get("identifier", control["type"]) == self._identifier:
                    return control.get("value")

        return None

    @property
    def state(self):
        """Return the current state of the cover."""
        value = self._get_control_state()
        if value == "OPEN":
            return STATE_OPEN
        if value == "CLOSED":
            return STATE_CLOSED
        if value == "MOVING":
            return STATE_OPENING
        return STATE_UNKNOWN

    @property
    def is_closed(self):
        """Return True if the cover is closed."""
        return self._get_control_state() == "CLOSED"

    @property
    def is_open(self):
        """Return True if the cover is open."""
        return self._get_control_state() == "OPEN"

    async def async_open_cover(self, **kwargs):
        """Send command to open the cover."""
        try:
            data = AutoDoorControl(zoneId=self._control.get("zoneId"), value=True)
            await self._api.set_value(self._device_id, self._control["name"], data)
            await asyncio.sleep(3)
        except Exception as e:
            _LOGGER.error("Failed to open door %s: %s", self._identifier, e)
        await self._coordinator.async_request_refresh()

    async def async_close_cover(self, **kwargs):
        """Send command to close the cover."""
        try:
            data = AutoDoorControl(zoneId=self._control.get("zoneId"), value=False)
            await self._api.set_value(self._device_id, self._control["name"], data)
            await asyncio.sleep(3)
        except Exception as e:
            _LOGGER.error("Failed to close door %s: %s", self._identifier, e)
        await self._coordinator.async_request_refresh()
