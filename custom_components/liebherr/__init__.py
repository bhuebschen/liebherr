"""Liebherr HomeAPI for HomeAssistant."""

from dataclasses import asdict
from datetime import timedelta
import json
import logging
from pathlib import Path
import ssl

import aiofiles
import aiohttp
from aiohttp import ClientSession, ClientTimeout, TCPConnector
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
import homeassistant.helpers.device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.util.dt import as_local, parse_datetime

# from homeassistant.core import __all__
from .const import (
    AIR_FILTER,
    BASE_API_URL,
    BASE_URL,
    DOMAIN,
    DOOR_ALARM,
    DOOR_OVERHEAT_ALARM,
    OBSTACLE_ALARM,
    POWER_FAILURE_ALARM,
    TEMPERATURE_ALARM,
)

_LOGGER = logging.getLogger(__name__)
_DEBUG = False


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Set up Liebherr devices from a config entry."""

    hass.data.setdefault(DOMAIN, {})
    api = LiebherrAPI(hass, config_entry.data)
    api.translations = await api.load_translations()

    ssl_context = await hass.async_add_executor_job(ssl.create_default_context)
    # DEBUG
    # ssl_context.check_hostname = False
    # ssl_context.verify_mode = ssl.CERT_NONE
    # api.connector = TCPConnector(ssl=ssl_context)
    ###
    api.connector = TCPConnector(ssl=ssl_context)

    api.session = ClientSession(
        connector=api.connector, timeout=ClientTimeout(total=10)
    )

    async def async_update_method() -> None:
        """Fetch both appliances and notifications."""

        _LOGGER.debug("async_update_method called")
        try:
            # Geräte abrufen
            appliances = await api.get_appliances()

            # Benachrichtigungen abrufen
            # await api.fetch_notifications(config_entry)
            filtered_notifications = []

            # Kombinierte Daten zurückgeben
            combined_data = {
                "appliances": appliances,
                "notifications": filtered_notifications,
            }
        except (LiebherrUpdateException, aiohttp.ClientError, TimeoutError) as e:
            raise UpdateFailed(f"Error updating Liebherr data: {e}") from e
        else:
            return combined_data

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="Liebherr devices",
        update_method=async_update_method,
        update_interval=timedelta(seconds=120),
    )
    _LOGGER.debug(
        "[LIEBHERR] Effective update interval: %s seconds",
        coordinator.update_interval.total_seconds(),
    )

    hass.data[DOMAIN][config_entry.entry_id] = {
        "api": api,
        "coordinator": coordinator,
    }

    # Raises ConfigEntryNotReady on failure -> HA retries setup in the
    # background with backoff instead of holding up startup.
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(
        config_entry, ["climate", "switch", "select", "sensor", "cover"]
    )
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(config_entry, "climate")
    await hass.config_entries.async_forward_entry_unload(config_entry, "switch")
    await hass.config_entries.async_forward_entry_unload(config_entry, "select")
    await hass.config_entries.async_forward_entry_unload(config_entry, "sensor")
    await hass.config_entries.async_forward_entry_unload(config_entry, "cover")
    hass.data[DOMAIN].pop(config_entry.entry_id)
    return True


class LiebherrAuthException(Exception):
    """Exception raised for authentication errors in the Liebherr API."""


class LiebherrUpdateException(Exception):
    """Exception raised for update methodes in the Liebherr API."""


class LiebherrFetchException(Exception):
    """Exception raised for fetching data in the Liebherr API."""


class LiebherrException(Exception):
    """Exception raised for errors in the Liebherr API."""

    def __init__(self, message) -> None:
        """Initialize the exception."""
        self.message = message

    def __str__(self):
        """Return the exception message."""
        return self.message


class LiebherrAPI:
    """Liebherr API Class."""

    def __init__(self, hass: HomeAssistant, config: dict) -> None:
        """Initialize the Liebherr HomeAPI."""
        self._hass = hass
        self.connector = {}
        self.session = {}
        self._key = config.get("api-key")
        self.translations = {}

    async def get_appliances(self):
        """Retrieve the list of appliances."""

        headers = {
            "api-key": self._key,
        }

        async with self.session.get(BASE_API_URL, headers=headers) as response:
            if response.status != 200:
                raise LiebherrUpdateException(
                    f"Failed to fetch appliances: {response.status}")

            data = await response.json()
            _LOGGER.debug("Fetched appliances: %s", data)
            return [
                {
                    "deviceId": appliance["deviceId"],
                    "model": appliance["deviceName"],
                    "image": appliance["imageUrl"],
                    "nickname": appliance.get("nickname", appliance["deviceName"]),
                    "applianceType": appliance["deviceType"],
                    # "capabilities": appliance["applianceInformation"]["capabilities"],
                    # "available": appliance["applianceInformation"].get(
                    #    "connected", True
                    # ),
                    "controls": await self.get_controls(appliance["deviceId"]),
                }
                for appliance in data
            ]

    async def get_controls(self, device_id):
        """Retrieve controls for a specific appliance."""
        url = f"{BASE_API_URL}/{device_id}/controls"
        headers = {
            "api-key": self._key,
        }

        async with self.session.get(url, headers=headers) as response:
            if response.status != 200:
                raise LiebherrUpdateException(
                    f"Failed to fetch controls for device {device_id}: {response.status}")
            if response.status == 401:
                _LOGGER.error("API-KEY provided is not valid")
                return []
            data = await response.json()
            _LOGGER.debug("Fetched controls for device %s: %s",
                          device_id, data)
            return data

    async def set_value(self, deviceId, control, value):
        """Activate or deactivate a control."""
        url = f"{BASE_API_URL}/{deviceId}/controls/{control}"
        headers = {
            "api-key": self._key,
            "Content-Type": "application/json",
        }
        payload = asdict(value)

        async with self.session.post(url, headers=headers, json=payload) as response:
            if response.status != 204:
                _LOGGER.error("Failed to set control: %s", response.status)

    async def get_notifications(self):
        """Retrieve notifications from the Liebherr API."""
        url = f"{BASE_URL}/notifications"
        headers = {
            "api-key": self._key,
            "Content-Type": "application/json",
        }

        try:
            async with self.session.get(url, headers=headers) as response:
                _LOGGER.debug("Fetching notifications: %s", response.status)
                if response.status == 200:
                    # Parse JSON response
                    _LOGGER.debug("Fetching notifications: %s", await response.text())
                    return await response.json()
                _LOGGER.error(
                    "Failed to fetch notifications: %s - %s",
                    response.status,
                    await response.text(),
                )
                if response.status == 401:
                    _LOGGER.error("API-KEY provided is not valid")

                return []
        except LiebherrFetchException as e:
            _LOGGER.error("Error fetching notifications: %s", e)
            return []

    async def fetch_notifications(self, config_entry):
        """Fetch notifications from the Liebherr API."""
        try:
            # Fetch all notifications from the API
            notifications = await self.get_notifications()

            # Get selected devices from options
            selected_devices = config_entry.options.get(
                "devices_to_notify", [])

            # Filter notifications for selected devices
            filtered_notifications = [
                notification
                for notification in notifications
                if notification["deviceId"] in selected_devices
                and not notification.get("isAcknowledged", False)
            ]

            # Process only filtered notifications
            await self.process_notifications(filtered_notifications)
        except LiebherrFetchException as e:
            _LOGGER.error("Error fetching notifications: %s", e)
        else:
            return filtered_notifications

    async def load_translations(self):
        """Load translations from the translations folder."""
        lang = self._hass.config.language  # Aktuelle Sprache des Benutzers
        translation_file = Path(__file__).parent / f"translations/{lang}.json"

        # Fallback zu Englisch, wenn die Sprache nicht verfügbar ist
        if not translation_file.is_file():
            translation_file = Path(__file__).parent / "translations/en.json"

        # Übersetzungen laden
        if translation_file.is_file():
            async with aiofiles.open(translation_file, encoding="utf-8") as file:
                content = await file.read()
                return json.loads(content)
        return {}

    def _translate(self, category, key):
        """Retrieve a translation for the given category and key."""
        return self.translations.get(category, {}).get(key, key)

    def _get_device_name(self, device_registry, device_id):
        """Get the device name based on the deviceId."""
        for device in device_registry.devices.values():
            # Prüfen, ob die Device-Id zu den Identifiers gehört
            if (DOMAIN, device_id) in device.identifiers:
                return device.name  # Name des Geräts zurückgeben
        return None  # Kein Name gefunden

    async def process_notifications(self, notifications):
        """Process notifications and create Home Assistant notifications."""

        device_registry = dr.async_get(self._hass)

        for notification in notifications:
            device_id = notification["deviceId"]
            device_name = self._get_device_name(device_registry, device_id)

            raw_created_at = notification.get("createdAt")
            created_at = None
            if raw_created_at:
                dt_obj = parse_datetime(raw_created_at)
                if dt_obj:
                    dt_local = as_local(dt_obj)
                    created_at = dt_local.strftime(
                        "%x %X"
                    )  # Lokale Formatierung (Datum und Zeit)

            notification_type = notification.get("notificationType", "unknown")
            notification_id = f"liebherr_{notification['notificationId']}"
            translated_notification_type = self._translate(
                "notificationType", notification_type
            )

            svg_icon = ""
            match notification["notificationType"]:
                case "door_alarm":
                    svg_icon = DOOR_ALARM
                case "air_filter_reminder":
                    svg_icon = AIR_FILTER
                case "upper_temperature_alarm", "lower_temperature_alarm":
                    svg_icon = TEMPERATURE_ALARM
                case "auto_door_overheat_alarm":
                    svg_icon = DOOR_OVERHEAT_ALARM
                case "auto_door_obstacle_alarm":
                    svg_icon = OBSTACLE_ALARM
                case "upper_power_failure_alarm", "lower_power_failure_alarm":
                    svg_icon = POWER_FAILURE_ALARM

            message = f"### {translated_notification_type} ({created_at if created_at else raw_created_at})\n"
            if svg_icon:
                message += f"![icon]({svg_icon})\n"
            self._hass.components.persistent_notification.create(
                message,
                title=f"{device_name or device_id}",
                notification_id=notification_id,
            )
            self._add_dismiss_listener(notification_id, notification)

    def _add_dismiss_listener(self, notification_id, notification):
        """Track when the notification is dismissed."""

        async def dismiss_handler(event):
            """Handle the dismiss event."""
            if event.data.get("notification_id") == notification_id:
                await self._acknowledge_notification(self, notification)
                self._hass.bus.async_listen(
                    "persistent_notification.dismiss", dismiss_handler
                ).remove()

        self._hass.bus.async_listen(
            "persistent_notification.dismiss", dismiss_handler)

    async def _acknowledge_notification(self, notification):
        """Send acknowledgment to the API."""
        try:
            url = f"https://mobile-api.smartdevice.liebherr.com/v1/household/notifications/{notification['deviceId']}/{notification['notificationId']}"
            await self.acknowledge_notification(url, notification["notificationId"])
        except LiebherrException as e:
            self._hass.components.persistent_notification.create(
                message=f"Failed to acknowledge notification(2): {e}",
                title="Liebherr Notification Error",
            )

    async def acknowledge_notification(self, device_id, notification_id):
        """Acknowledge a notification."""
        url = f"{BASE_API_URL}/notifications/{device_id}/{notification_id}"
        headers = {
            "api-key": self._key,
            "Content-Type": "application/json",
        }
        payload = {"isAcknowledged": True}

        async with self.session.patch(url, headers=headers, json=payload) as response:
            if response.status == 204:
                _LOGGER.info(
                    "Successfully acknowledged notification %s for device %s",
                    notification_id,
                    device_id,
                )
                return True
            _LOGGER.error(
                "Failed to acknowledge notification(1) %s: %s",
                notification_id,
                response.status,
            )
            return False


class LiebherrConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Liebherr Integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="Liebherr HomeAPI", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required("api-key"): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={"help_text": ""},
        )
