"""Support for Liebherr sensors."""

import logging
from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities
):
    """Set up sensors."""
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
            zone_id = control.get("zoneId", 0)
            control_type = control.get("type")

            # Define known sensors
            sensor_map = {
                "biofresh": {
                    "attribute": "current",
                    "unit": "°C",
                    "device_class": SensorDeviceClass.TEMPERATURE,
                    "icon": "mdi:thermometer",
                },
                "autodoorcontrol": {
                    "attribute": "value",
                    "unit": None,
                    "device_class": None,
                    "icon": "mdi:door-open",
                },
                "hydrobreeze": {
                    "attribute": "currentMode",
                    "unit": None,
                    "device_class": None,
                    "icon": "mdi:air-humidifier",
                },
            }

            config = sensor_map.get(control_type.lower())
            if config:
                entities.append(
                    LiebherrSensor(
                        api,
                        coordinator,
                        appliance,
                        control,
                        zone_id,
                        config["attribute"],
                        config["unit"],
                        config["device_class"],
                        config["icon"],
                    )
                )
            else:
                _LOGGER.debug("Unsupported sensor type: %s", control_type)

    async_add_entities(entities)


class LiebherrSensor(SensorEntity):
    """Representation of a Liebherr sensor entity."""

    def __init__(
        self,
        api,
        coordinator,
        appliance,
        control,
        zone_id,
        attribute,
        unit,
        device_class,
        icon,
        enabled_default=True,
    ):
        """Initialize the sensor entity."""
        self._api = api
        self._coordinator = coordinator
        self._appliance = appliance
        self._control = control
        self._zone_id = control.get("zoneId", zone_id)
        self._attribute = attribute
        self._unit = unit
        self._device_class = device_class
        self._icon = icon
        self._enabled_default = enabled_default

        self._identifier = control.get("identifier", control["type"])
        self._device_id = appliance["deviceId"]

        nickname = appliance.get("nickname", "Liebherr")
        self._attr_name = f"{nickname} {self._identifier} {attribute}"
        if self._zone_id:
            self._attr_name += f" Zone {self._zone_id}"

        self._attr_unique_id = f"{DOMAIN}_{self._device_id}_{self._identifier}_{attribute}_zone{self._zone_id}"
        self._attr_entity_registry_enabled_default = enabled_default

    @property
    def device_info(self):
        """Return device information for the sensor."""
        return {
            "identifiers": {(DOMAIN, self._device_id)},
            "name": self._appliance.get("nickname", f"Liebherr Appliance {self._device_id}"),
            "manufacturer": "Liebherr",
            "model": self._appliance.get("model"),
            "sw_version": self._appliance.get("softwareVersion", ""),
        }

    def _get_current_value(self):
        """Get the most recent value from the coordinator."""
        data = self._coordinator.data or {}
        for device in data.get("appliances", []):
            if device.get("deviceId") != self._device_id:
                continue
            for control in device.get("controls", []):
                if (
                    control.get("identifier", control["type"]) == self._identifier
                    and control.get("zoneId", 0) == self._zone_id
                ):
                    return control.get(self._attribute)
        return None
        
    @property
    def state(self):
        """Return the state of the sensor."""
        value = self._get_current_value()

        if value == "MOVING":
            # Schedule another update in 5 seconds
            self.hass.loop.create_task(self._delayed_refresh())

        return value

    async def _delayed_refresh(self):
        """Force refresh after delay if moving detected."""
        await asyncio.sleep(30)
        await self._coordinator.async_request_refresh()


    @property
    def unit_of_measurement(self):
        """Return the unit_of_measurement of the sensor"""
        return self._unit

    @property
    def device_class(self):
        """Return the device_class of the sensor."""
        return self._device_class

    @property
    def available(self):
        """Return True if the sensor is available."""
        return True

    async def async_update(self):
        """Fetch new state data for the sensor."""
        await asyncio.sleep(30)
        await self._coordinator.async_request_refresh()

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon
