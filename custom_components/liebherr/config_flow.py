"""Config flow for Liebherr Integration."""

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import config_validation as cv
import homeassistant.helpers.device_registry as dr

from .const import DOMAIN


class LiebherrConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Liebherr Integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title="Liebherr SmartDevice", data=user_input
            )

        data_schema = vol.Schema(
            {
                vol.Required("api-key"): str,
            }
        )
        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Return the options flow handler."""
        return LiebherrOptionsFlow(config_entry)


class LiebherrOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Liebherr Integration."""

    def __init__(self, config_entry) -> None:
        """Initialize the options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            # Save the options
            return self.async_create_entry(title="", data=user_input)

        # Dynamically create the multi-select options schema based on devices
        device_registry = dr.async_get(self.hass)
        devices = [
            device
            for device in device_registry.devices.values()
            if DOMAIN in {id_tuple[0] for id_tuple in device.identifiers}
        ]

        # Map device IDs to nicknames for the multi-select
        devices_for_notify = {
            next(iter(device.identifiers))[
                1
            ]: f"{device.name or 'Unknown'} ({device.id})"
            for device in devices
        }

        # Create the schema with a multi-select field
        options_schema = vol.Schema(
            {
                vol.Optional(
                    "devices_to_notify",
                    default=list(
                        devices_for_notify.keys()
                    ),  # Default: all devices selected
                ): cv.multi_select(devices_for_notify)
            }
        )

        # Display the form with the dynamically created schema
        return self.async_show_form(
            step_id="init",
            data_schema=options_schema,
        )
