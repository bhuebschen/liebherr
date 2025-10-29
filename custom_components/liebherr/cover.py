"""Support for Liebherr autodoor devices with debounce logic."""

import asyncio
import logging
from datetime import datetime, timedelta

from homeassistant.components.cover import CoverEntity, CoverEntityFeature
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import STATE_OPEN, STATE_CLOSED, STATE_OPENING, STATE_UNKNOWN

from .const import DOMAIN
from .models import AutoDoorControl

_LOGGER = logging.getLogger(__name__)

DEBOUNCE_SECONDS = 30  # time to wait before confirming final door state


async def async_setup_entry(
    hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities
):
    """Set up Liebherr covers from a config entry."""
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
            if control["type"] == "AutoDoorControl":
                entities.append(LiebherrCover(api, coordinator, appliance, control))

    async_add_entities(entities)


class LiebherrCover(CoverEntity):
    """Representation of a Liebherr auto door cover with debounce."""

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

        # For debounce:
        self._last_state = None
        self._last_state_change = None
        self._debounce_task = None
        self._confirmed_state = STATE_UNKNOWN

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

    async def _debounce_state(self, new_state):
        """Debounce door state changes to avoid flickering."""
        # Cancel existing debounce task if any
        if self._debounce_task and not self._debounce_task.done():
            self._debounce_task.cancel()

        # If door is MOVING, update immediately but do not confirm
        if new_state == "MOVING":
            self._confirmed_state = STATE_OPENING
            self.async_write_ha_state()
            return

        # If state changed from last confirmed state, start debounce delay
        if new_state != self._confirmed_state:
            self._last_state = new_state
            self._last_state_change = datetime.now()

            async def wait_and_confirm():
                try:
                    await asyncio.sleep(DEBOUNCE_SECONDS)
                    # After waiting, confirm the new state
                    self._confirmed_state = (
                        STATE_OPEN if new_state == "OPEN" else STATE_CLOSED
                    )
                    self.async_write_ha_state()
                except asyncio.CancelledError:
                    # Debounce canceled because new update arrived
                    pass

            self._debounce_task = asyncio.create_task(wait_and_confirm())

    @property
    def state(self):
        """Return the current debounced state of the cover."""
        return self._confirmed_state

    @property
    def is_closed(self):
        """Return True if the cover is closed."""
        return self._confirmed_state == STATE_CLOSED

    @property
    def is_open(self):
        """Return True if the cover is open."""
        return self._confirmed_state == STATE_OPEN

    async def async_open_cover(self, **kwargs):
        """Send command to open the cover."""
        try:
            data = AutoDoorControl(zoneId=self._control.get("zoneId"), value=True)
            await self._api.set_value(self._device_id, self._control["name"], data)
            await asyncio.sleep(30)  # Let the door start moving
        except Exception as e:
            _LOGGER.error("Failed to open door %s: %s", self._identifier, e)
        await asyncio.sleep(30)
        await self._coordinator.async_request_refresh()

    async def async_close_cover(self, **kwargs):
        """Send command to close the cover."""
        try:
            data = AutoDoorControl(zoneId=self._control.get("zoneId"), value=False)
            await self._api.set_value(self._device_id, self._control["name"], data)
            await asyncio.sleep(30)  # Let the door start moving
        except Exception as e:
            _LOGGER.error("Failed to close door %s: %s", self._identifier, e)
        await asyncio.sleep(30)
        await self._coordinator.async_request_refresh()

    async def async_update(self):
        """Called by coordinator on data update; update state with debounce."""
        raw_state = self._get_control_state()
        if raw_state is None:
            self._confirmed_state = STATE_UNKNOWN
            self.async_write_ha_state()
            return
        await self._debounce_state(raw_state)
