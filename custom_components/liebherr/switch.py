"""Support for Liebherr mode switches."""

import asyncio
import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .models import BaseToggleControlRequest, ZoneToggleControlRequest, IceMakerControlRequest

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities
):
    """Set up Liebherr switches from a config entry."""
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
            zone_id = control.get("zoneId") or 0
            if control["type"] in ("ToggleControl"):
                entities.extend(
                    [
                        LiebherrSwitch(api, coordinator, appliance, control, zone_id),
                    ]
                )

    if not entities:
        _LOGGER.error("No switch entities created")

    async_add_entities(entities)


class LiebherrSwitch(SwitchEntity):
    """Representation of a Liebherr switch entity."""

    def __init__(self, api, coordinator, appliance, control, zoneId) -> None:
        """Initialize the switch entity."""
        self._api = api
        self._coordinator = coordinator
        self._appliance = appliance
        self._control = control
        self._zoneId = zoneId
        self._identifier = (
            appliance.get("nickname") + "_" +
            control.get("name", control.get("type"))
        )
        if "zonePosition" in control:
            self._identifier += f"_{control['zonePosition']}"
        elif "zoneId" in control:
            self._identifier += f"_{control['zoneId']}"
        self._control_name = control.get("name")
        self._attr_name = appliance.get("nickname") + " " + control.get("name")
        if "zonePosition" in control:
            self._attr_name += f" {control['zonePosition']}"
        elif "zoneId" in control:
            self._attr_name += f" {control['zoneId']}"
        self._attr_unique_id = "liebherr_" + self._identifier
        self._attr_icon = self._get_icon(self._control_name.lower())

    def _get_icon(self, name: str) -> str | None:
        return {
            "supercool": "mdi:snowflake",
            "superfrost": "mdi:snowflake-variant",
            "partymode": "mdi:party-popper",
            "holidaymode": "mdi:beach",
            "nightmode": "mdi:weather-night",
            "bottletimer": "mdi:timer-sand",
        }.get(name)

    @property
    def device_info(self):
        """Return device information for the switch."""
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
    def is_on(self):
        """Return true if the switch is on."""
        if not self._coordinator.data:
            _LOGGER.error("Coordinator data is empty")
            return False

        controls = []
        appliances = self._coordinator.data.get("appliances", [])
        for device in appliances:
            if device.get("deviceId") == self._appliance["deviceId"]:
                controls = device.get("controls", [])
                for control in controls:
                    if self._control_name == control.get("name"):
                        if self._zoneId == control.get("zoneId"):
                            _LOGGER.debug(control)
                            control_type = control.get("type")
                            # Handle control types individually
                            if control_type == "ToggleControl":
                                return control.get("value") is True
                            else:
                                _LOGGER.warning(
                                    "Unsupported control type '%s' for control '%s'",
                                    control_type, self._control_name
                                )
                                return False
        return False

    def setControlValue(self, value):
        """Change controls value."""
        appliances = self._coordinator.data.get("appliances", [])
        device = next(
            (d for d in appliances if d.get("deviceId")
             == self._appliance["deviceId"]),
            None,
        )

        if device:
            control = next(
                (
                    c
                    for c in device.get("controls", [])
                    if self._control_name == c.get("name")
                    and self._zoneId == c.get("zoneId")
                ),
                None,
            )
            if control:
                control["value"] = value

    @property
    def available(self):
        """Return True if the switch is available."""
        return True

    async def async_turn_on(self, **kwargs):
        """Turn the switch on."""
        if self._control["type"] == "BottleTimer":
            await self._api.set_value(
                self._appliance["deviceId"] + "/" + self._control["name"],
                {"bottleTimer": "ON"},
            )
        if self._control["type"] == "AutoDoor":
            await self._api.set_value(
                self._appliance["deviceId"] + "/" + self._control["name"],
                {"bottleTimer": "ON"},
            )
        if self._control["type"] == "ToggleControl":
            if self._control.get("zoneId", None) is None:
                data = BaseToggleControlRequest(value=True)
            else:
                data = ZoneToggleControlRequest(
                    zoneId=self._control.get("zoneId"), value=True
                )

            await self._api.set_value(
                self._appliance["deviceId"], self._control["name"], data
            )
            self.setControlValue(True)

    async def async_turn_off(self, **kwargs):
        """Turn the switch off."""
        if self._control["type"] == "bottletimer":
            await self._api.set_value(
                self._appliance["deviceId"] + "/" + self._control["name"],
                {"bottleTimer": "OFF"},
            )
        if self._control["type"] == "ToggleControl":
            if self._control.get("zoneId", None) is None:
                data = BaseToggleControlRequest(value=False)
            else:
                data = ZoneToggleControlRequest(
                    zoneId=self._control.get("zoneId"), value=False
                )

            await self._api.set_value(
                self._appliance["deviceId"], self._control["name"], data
            )
            self.setControlValue(False)
