from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
import logging
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up sensors."""
    api = hass.data[DOMAIN][config_entry.entry_id]["api"]
    coordinator = hass.data[DOMAIN][config_entry.entry_id]["coordinator"]

    appliances = await api.get_appliances()

    entities = []
    for appliance in appliances:
        # TODO: appliance connection state

        controls = await api.get_controls(appliance["deviceId"])
        if not controls:
            _LOGGER.warning("No controls found for appliance %s",
                            appliance["deviceId"])
            continue

        for control in controls:
            match control["controlType"]:
                case "biofresh":
                    entities.append(LiebherrSensor(
                        api, coordinator, appliance, control, 'current', '°C', SensorDeviceClass.TEMPERATURE, 'mdi:thermometer'))
                case "autodoor":
                    entities.append(LiebherrSensor(
                        api, coordinator, appliance, control, 'enabled', None, None, 'mdi:toggle-switch-off-outline', enabled_default = False))
                    entities.append(LiebherrSensor(
                        api, coordinator, appliance, control, 'calibrated', None, None, 'mdi:door', enabled_default = False))
                    entities.append(LiebherrSensor(
                        api, coordinator, appliance, control, 'doorState', None, None, 'mdi:door-open'))
                case "hydrobreeze":
                    entities.append(LiebherrSensor(
                        api, coordinator, appliance, control, 'currentMode', None, None, 'mdi:air-humidifier'))

    if not entities:
        _LOGGER.error("No sensor entities created")

    async_add_entities(entities)


class LiebherrSensor(SensorEntity):
    """Representation of a Liebherr sensor entity."""
    should_poll = True

    def __init__(self, api, coordinator, appliance, control, attribute, sensor_type, device_class, icon, enabled_default = True) -> None:
        """Initialize the sensor entity."""
        self._api = api
        self._coordinator = coordinator
        self._appliance = appliance
        self._control = control
        self._identifier = control.get("identifier", control["controlType"])
        self._attr_name = f"{appliance['nickname']} {self._identifier}"
        self._attr_unique_id = f"{appliance['deviceId']}_{self._identifier}"
        self._attribute = attribute
        self._endpoint = control.get("endpoint")
        self._sensor_type = sensor_type
        self._device_class = device_class
        self._icon = icon
        self._attr_state = None
        self._attr_entity_registry_enabled_default = enabled_default

    @property
    def device_info(self):
        """Return device information for the sensor."""
        return {
            "identifiers": {(DOMAIN, self._appliance["deviceId"])},
            "name": self._appliance.get(
                "nickname", f"Liebherr Device {self._appliance['deviceId']}"
            ),
            "manufacturer": "Liebherr",
            "model": self._appliance.get("model", self._appliance["model"]),
            "sw_version": self._appliance.get("softwareVersion", ""),
            "configuration_url": self._appliance.get("image", ""),
        }

    @property
    def state(self):
        """Return the state of the sensor."""
        if not self._coordinator.data:
            _LOGGER.error("Coordinator data is empty")
            return None

        return self._control.get(self._attribute)

    @property
    def unit_of_measurement(self):
        """Return the unit_of_measurement of the sensor."""
        return self._sensor_type

    @property
    def device_class(self):
        """Return the device_class of the sensor."""
        return self._device_class

    def available(self):
        """Return True if the sensor is available."""
        return self._appliance["available"]

    async def async_update(self):
        """Fetch new state data for the sensor."""
        await self._coordinator.async_request_refresh()

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon
