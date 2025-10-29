"""Support for Liebherr mode selections."""

import asyncio
import logging
from typing import Callable

from homeassistant.components.select import SelectEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .models import ModeControlRequest, IceMakerControlRequest

_LOGGER = logging.getLogger(__name__)

# Control configuration
SELECT_CONFIG: dict[str, dict] = {
    "biofreshplus": {
        "icon": "mdi:leaf",
        "options": None,
        "user-options": None,
        "attr": "currentMode",
    },
    "hydrobreeze": {
        "icon": "mdi:water",
        "options": ["OFF", "LOW", "MEDIUM", "HIGH"],
        "user-options": ["Off", "Low", "Medium", "High"],
        "attr": "currentMode",
    },
    "icemaker": {
        "icon": "mdi:cube-outline",
        "options": lambda ctrl: ["OFF", "ON", "MAX_ICE"] if ctrl.get("hasMaxIce") else ["OFF", "ON"],
        "user-options": lambda ctrl: ["Off", "On", "Max Ice"] if ctrl.get("hasMaxIce") else ["Off", "On"],
        "attr": "iceMakerMode",
    },
}


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities
):
    """Set up Liebherr selects from a config entry."""
    api = hass.data[DOMAIN][config_entry.entry_id]["api"]
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    await asyncio.sleep(30)
    appliances = await api.get_appliances()
    entities = []

    for appliance in appliances:
        await asyncio.sleep(30)
        controls = await api.get_controls(appliance["deviceId"])
        if not controls:
            _LOGGER.warning("No controls found for appliance %s", appliance["deviceId"])
            continue

        for control in controls:
            ctrl_name = control.get("name", control.get("type"))
            if ctrl_name in SELECT_CONFIG:
                entities.append(LiebherrSelect(api, coordinator, appliance, control))

    async_add_entities(entities)


class LiebherrSelect(SelectEntity):
    """Representation of a Liebherr select entity."""

    def __init__(self, api, coordinator, appliance, control) -> None:
        """Initialize the select entity."""
        self._api = api
        self._coordinator = coordinator
        self._appliance = appliance
        self._control = control

        self._identifier = control.get("name", control.get("type"))
        self._device_id = appliance["deviceId"]

        nickname = appliance.get("nickname", "Liebherr")
        self._attr_name = f"{nickname} {self._identifier}"
        self._attr_unique_id = f"{self._device_id}_{self._identifier}"

        config = SELECT_CONFIG.get(self._identifier, {})

        self._attr_icon = config.get("icon")
        self._state_attr_key = config.get("attr", "currentMode")

        # Raw options sent to the API
        raw_options = config.get("options")
        if callable(raw_options):
            raw_options = raw_options(control)

        # Pretty options shown to user
        user_options = config.get("user-options")
        if callable(user_options):
            user_options = user_options(control)

        self._raw_to_user = dict(zip(raw_options, user_options))
        self._user_to_raw = dict(zip(user_options, raw_options))
        self._attr_options = user_options

    def _format_label(self, value: str) -> str:
        """Format raw option label to user-friendly form."""
        return value.capitalize().replace("_", "")

    @property
    def device_info(self):
        """Return device information for the select."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._appliance.get("nickname", f"Liebherr {self._device_id}"),
            "manufacturer": "Liebherr",
            "model": self._appliance.get("model", self._appliance["model"]),
            "sw_version": self._appliance.get("softwareVersion", ""),
        }

    def _get_control_from_coordinator(self):
        """Return the current control from the coordinator data."""
        if not self._coordinator.data:
            _LOGGER.error("Coordinator data is empty")
            return None

        for device in self._coordinator.data.get("appliances", []):
            if device.get("deviceId") != self._device_id:
                continue
            for control in device.get("controls", []):
                if control.get("name", control.get("type")) == self._identifier:
                    return control
        return None

    @property
    def current_option(self):
        """Return the current selected option."""
        control = self._get_control_from_coordinator()
        if not control:
            return None
        raw_value = control.get(self._state_attr_key)
        return self._raw_to_user.get(raw_value, raw_value)

    async def async_select_option(self, option: str):
        """Change the selected option."""
        if option not in self._user_to_raw:
            _LOGGER.error("Invalid option selected: %s", option)
            return

        raw_value = self._user_to_raw[option]

        try:
            if self._control["type"] == "IceMakerControl":
                data = IceMakerControlRequest(
                    zoneId=self._control.get("zoneId"),
                    iceMakerMode=raw_value,
                )
            else:
                data = ModeControlRequest(mode=raw_value)

            await self._api.set_value(
                self._device_id,
                self._control["name"],
                data,
            )

            await asyncio.sleep(30)

        except Exception as e:
            _LOGGER.error("Failed to set option '%s' for '%s': %s", option, self._identifier, e)
            return

        await self._coordinator.async_request_refresh()
        await asyncio.sleep(30)
