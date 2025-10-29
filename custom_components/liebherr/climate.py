"""Support for Liebherr appliances as climate devices."""

import asyncio
import logging

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
)
from homeassistant.const import ATTR_TEMPERATURE
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .models import TemperatureControlRequest

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, config_entry, async_add_entities):
    """Set up Liebherr appliances as devices and entities from a config entry."""
    api = hass.data[DOMAIN][config_entry.entry_id]["api"]
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    await asyncio.sleep(30)
    appliances = await api.get_appliances()
    entities = []
    for appliance in appliances:
        await asyncio.sleep(30)
        controls = await api.get_controls(appliance["deviceId"])
        if not controls:
            _LOGGER.warning("No controls found for appliance %s",
                            appliance["deviceId"])
            continue

        if appliance["applianceType"] in [
            "FRIDGE",
            "FREEZER",
            "COMBI",
            "WINE",
        ]:
            for control in controls:
                if control.get("type") == "TemperatureControl":
                    _LOGGER.debug(
                        "Adding climate entity for %s",
                        appliance.get("deviceId")
                        + "_"
                        + control.get("name", control.get("type"))
                        + "_"
                        + control.get("zonePosition"),
                    )
                    entities.append(
                        LiebherrClimate(
                            coordinator,
                            api,
                            appliance,
                            control,
                            control.get("zoneId"),
                        )
                    )

    async_add_entities(entities)


class LiebherrClimate(ClimateEntity):
    """Representation of a Liebherr climate entity."""

    def __init__(self, coordinator, api, appliance, control, zoneId) -> None:
        """Initialize the climate entity."""
        self.coordinator = coordinator
        self.api = api
        self._control = control
        self._identifier = (
            appliance.get("nickname")
            + "_"
            + control.get("name", control.get("type"))
            + "_"
            + control.get("zonePosition", str(control.get("zoneId", zoneId)))
        )
        self._appliance = appliance
        self._zoneId = control.get("zoneId", zoneId)
        self._control_name = control.get("name")
        self._attr_name = (
            appliance.get("nickname")
            + " "
            + control.get("name")
            + " "
            + control.get("zonePosition", str(control.get("zoneId", zoneId)))
        )
        self._attr_unique_id = "liebherr_" + self._identifier
        self._attr_target_temperature_step = 1
        self._attr_temperature_unit = control.get("unit")
        self._attr_supported_features = ClimateEntityFeature.TARGET_TEMPERATURE
        self._attr_hvac_modes = [HVACMode.COOL]
        self._attr_hvac_mode = HVACMode.COOL

    @property
    def device_info(self):
        """Return device information for the appliance."""
        return {
            "identifiers": {(DOMAIN, self._appliance["deviceId"])},
            "name": self._appliance.get(
                "nickname", f"Liebherr HomeAPI Appliance {self._appliance['deviceId']}"
            ),
            "manufacturer": "Liebherr",
            "model": self._appliance.get("model", "Unknown Model"),
            "sw_version": self._appliance.get("softwareVersion", ""),
        }

    async def async_set_temperature(self, **kwargs):
        """Set the target temperature."""
        if ATTR_TEMPERATURE in kwargs:
            temperature = kwargs[ATTR_TEMPERATURE]

            self._attr_target_temperature = temperature
            self.async_write_ha_state()

            data = TemperatureControlRequest(
                zoneId=self._zoneId,
                target=temperature,
                unit=self._attr_temperature_unit,
            )

            await self.api.set_value(self._appliance["deviceId"], "temperature", data)
            await asyncio.sleep(30)
            await self.coordinator.async_request_refresh()

    @property
    def target_temperature(self):
        """Return the target temperature."""
        appliances = self.coordinator.data.get("appliances", [])
        for device in appliances:
            if device.get("deviceId") == self._appliance["deviceId"]:
                controls = device.get("controls", [])
                for control in controls:
                    if self._control_name == control.get("name"):
                        if self._zoneId == control.get("zoneId"):
                            return float(control.get("target"))
        return None

    @property
    def min_temp(self):
        """Return the minimum temperature that can be set."""
        appliances = self.coordinator.data.get("appliances", [])
        for device in appliances:
            if device.get("deviceId") == self._appliance["deviceId"]:
                controls = device.get("controls", [])
                for control in controls:
                    if self._control_name == control.get("name"):
                        if self._zoneId == control.get("zoneId"):
                            return float(control.get("min"))
        return None

    @property
    def max_temp(self):
        """Return the maximum temperature that can be set."""
        appliances = self.coordinator.data.get("appliances", [])
        for device in appliances:
            if device.get("deviceId") == self._appliance["deviceId"]:
                controls = device.get("controls", [])
                for control in controls:
                    if self._control_name == control.get("name"):
                        if self._zoneId == control.get("zoneId"):
                            return float(control.get("max"))
        return None

    @property
    def current_temperature(self):
        """Return the current temperature."""
        appliances = self.coordinator.data.get("appliances", [])
        for device in appliances:
            if device.get("deviceId") == self._appliance["deviceId"]:
                controls = device.get("controls", [])
                for control in controls:
                    if self._control_name == control.get("name"):
                        if self._zoneId == control.get("zoneId"):
                            return float(control.get("value"))
        return None

    @property
    def hvac_mode(self):
        """Return the current HVAC mode."""
        return self._attr_hvac_mode

    async def async_set_hvac_mode(self, hvac_mode):
        """Set the HVAC mode."""
        if hvac_mode in self._attr_hvac_modes:
            self._attr_hvac_mode = hvac_mode
            await asyncio.sleep(30)
            await self.coordinator.async_request_refresh()

    async def async_update(self):
        """Fetch the latest data from the API."""
        await asyncio.sleep(30)
        await self.coordinator.async_request_refresh()
