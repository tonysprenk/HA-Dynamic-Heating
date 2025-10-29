“”“Config flow for Dynamic Heating Scheduler.”””
from **future** import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.helpers.selector import (
EntitySelector,
EntitySelectorConfig,
NumberSelector,
NumberSelectorConfig,
NumberSelectorMode,
SelectSelector,
SelectSelectorConfig,
SelectSelectorMode,
TimeSelector,
)

from .const import (
CONF_COMFORT_END,
CONF_COMFORT_START,
CONF_COMFORT_TEMP,
CONF_ENABLE_COP_OPTIMIZATION,
CONF_HOME_AWAY_SENSOR,
CONF_OUTDOOR_TEMP_SENSOR,
CONF_OUTDOOR_TEMP_THRESHOLD,
CONF_PRICE_SENSOR,
CONF_TEMP_AWAY,
CONF_TEMP_BOOST,
CONF_TEMP_MAX,
CONF_TEMP_MIN,
CONF_TEMP_NORMAL,
CONF_TEMP_SETBACK,
CONF_ZONE_CLIMATE,
CONF_ZONE_NAME,
CONF_ZONES,
DEFAULT_COMFORT_END,
DEFAULT_COMFORT_START,
DEFAULT_COMFORT_TEMP,
DEFAULT_ENABLE_COP_OPTIMIZATION,
DEFAULT_OUTDOOR_TEMP_THRESHOLD,
DEFAULT_TEMP_AWAY,
DEFAULT_TEMP_BOOST,
DEFAULT_TEMP_MAX,
DEFAULT_TEMP_MIN,
DEFAULT_TEMP_NORMAL,
DEFAULT_TEMP_SETBACK,
DOMAIN,
)

_LOGGER = logging.getLogger(**name**)

class DynamicHeatingConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
“”“Handle a config flow for Dynamic Heating Scheduler.”””

```
VERSION = 1

def __init__(self):
    """Initialize the config flow."""
    self._zones = []
    self._current_zone = {}
    self._base_config = {}

async def async_step_user(
    self, user_input: dict[str, Any] | None = None
) -> config_entries.FlowResult:
    """Handle the initial step."""
    errors = {}

    if user_input is not None:
        self._base_config = user_input
        return await self.async_step_global_settings()

    data_schema = vol.Schema(
        {
            vol.Required(CONF_NAME, default="Dynamic Heating"): str,
            vol.Required(CONF_PRICE_SENSOR): EntitySelector(
                EntitySelectorConfig(domain=["sensor"])
            ),
        }
    )

    return self.async_show_form(
        step_id="user",
        data_schema=data_schema,
        errors=errors,
    )

async def async_step_global_settings(
    self, user_input: dict[str, Any] | None = None
) -> config_entries.FlowResult:
    """Handle global settings."""
    errors = {}

    if user_input is not None:
        self._base_config.update(user_input)
        return await self.async_step_add_zone()

    data_schema = vol.Schema(
        {
            vol.Optional(CONF_OUTDOOR_TEMP_SENSOR): EntitySelector(
                EntitySelectorConfig(domain=["sensor"])
            ),
            vol.Optional(CONF_HOME_AWAY_SENSOR): EntitySelector(
                EntitySelectorConfig(domain=["binary_sensor", "input_boolean"])
            ),
            vol.Required(
                CONF_TEMP_BOOST, default=DEFAULT_TEMP_BOOST
            ): NumberSelector(
                NumberSelectorConfig(
                    min=15, max=30, step=0.5, mode=NumberSelectorMode.SLIDER
                )
            ),
            vol.Required(
                CONF_TEMP_NORMAL, default=DEFAULT_TEMP_NORMAL
            ): NumberSelector(
                NumberSelectorConfig(
                    min=15, max=30, step=0.5, mode=NumberSelectorMode.SLIDER
                )
            ),
            vol.Required(
                CONF_TEMP_SETBACK, default=DEFAULT_TEMP_SETBACK
            ): NumberSelector(
                NumberSelectorConfig(
                    min=15, max=30, step=0.5, mode=NumberSelectorMode.SLIDER
                )
            ),
            vol.Required(
                CONF_TEMP_AWAY, default=DEFAULT_TEMP_AWAY
            ): NumberSelector(
                NumberSelectorConfig(
                    min=10, max=25, step=0.5, mode=NumberSelectorMode.SLIDER
                )
            ),
            vol.Required(CONF_TEMP_MIN, default=DEFAULT_TEMP_MIN): NumberSelector(
                NumberSelectorConfig(
                    min=10, max=20, step=0.5, mode=NumberSelectorMode.SLIDER
                )
            ),
            vol.Required(CONF_TEMP_MAX, default=DEFAULT_TEMP_MAX): NumberSelector(
                NumberSelectorConfig(
                    min=20, max=30, step=0.5, mode=NumberSelectorMode.SLIDER
                )
            ),
            vol.Required(
                CONF_COMFORT_START, default=DEFAULT_COMFORT_START
            ): TimeSelector(),
            vol.Required(
                CONF_COMFORT_END, default=DEFAULT_COMFORT_END
            ): TimeSelector(),
            vol.Required(
                CONF_COMFORT_TEMP, default=DEFAULT_COMFORT_TEMP
            ): NumberSelector(
                NumberSelectorConfig(
                    min=15, max=30, step=0.5, mode=NumberSelectorMode.SLIDER
                )
            ),
            vol.Required(
                CONF_ENABLE_COP_OPTIMIZATION, default=DEFAULT_ENABLE_COP_OPTIMIZATION
            ): selector.BooleanSelector(),
            vol.Optional(
                CONF_OUTDOOR_TEMP_THRESHOLD, default=DEFAULT_OUTDOOR_TEMP_THRESHOLD
            ): NumberSelector(
                NumberSelectorConfig(
                    min=-20, max=10, step=1, mode=NumberSelectorMode.SLIDER
                )
            ),
        }
    )

    return self.async_show_form(
        step_id="global_settings",
        data_schema=data_schema,
        errors=errors,
    )

async def async_step_add_zone(
    self, user_input: dict[str, Any] | None = None
) -> config_entries.FlowResult:
    """Handle adding a heating zone."""
    errors = {}

    if user_input is not None:
        if user_input.get("add_another"):
            self._zones.append(self._current_zone.copy())
            self._current_zone = {}
            return await self.async_step_zone_config()
        else:
            if self._current_zone:
                self._zones.append(self._current_zone.copy())
            
            # Create the config entry
            self._base_config[CONF_ZONES] = self._zones
            
            return self.async_create_entry(
                title=self._base_config[CONF_NAME],
                data=self._base_config,
            )

    if not self._zones and not self._current_zone:
        return await self.async_step_zone_config()

    data_schema = vol.Schema(
        {
            vol.Required("add_another", default=True): selector.BooleanSelector(),
        }
    )

    return self.async_show_form(
        step_id="add_zone",
        data_schema=data_schema,
        errors=errors,
        description_placeholders={
            "zone_count": str(len(self._zones) + (1 if self._current_zone else 0))
        },
    )

async def async_step_zone_config(
    self, user_input: dict[str, Any] | None = None
) -> config_entries.FlowResult:
    """Configure a heating zone."""
    errors = {}

    if user_input is not None:
        self._current_zone = user_input
        return await self.async_step_add_zone()

    data_schema = vol.Schema(
        {
            vol.Required(CONF_ZONE_NAME): str,
            vol.Required(CONF_ZONE_CLIMATE): EntitySelector(
                EntitySelectorConfig(domain=["climate"])
            ),
        }
    )

    return self.async_show_form(
        step_id="zone_config",
        data_schema=data_schema,
        errors=errors,
    )

@staticmethod
@callback
def async_get_options_flow(
    config_entry: config_entries.ConfigEntry,
) -> config_entries.OptionsFlow:
    """Get the options flow for this handler."""
    return DynamicHeatingOptionsFlow(config_entry)
```

class DynamicHeatingOptionsFlow(config_entries.OptionsFlow):
“”“Handle options flow for Dynamic Heating Scheduler.”””

```
def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
    """Initialize options flow."""
    self.config_entry = config_entry

async def async_step_init(
    self, user_input: dict[str, Any] | None = None
) -> config_entries.FlowResult:
    """Manage the options."""
    if user_input is not None:
        return self.async_create_entry(title="", data=user_input)

    data_schema = vol.Schema(
        {
            vol.Required(
                CONF_TEMP_BOOST,
                default=self.config_entry.data.get(CONF_TEMP_BOOST, DEFAULT_TEMP_BOOST),
            ): NumberSelector(
                NumberSelectorConfig(
                    min=15, max=30, step=0.5, mode=NumberSelectorMode.SLIDER
                )
            ),
            vol.Required(
                CONF_TEMP_NORMAL,
                default=self.config_entry.data.get(CONF_TEMP_NORMAL, DEFAULT_TEMP_NORMAL),
            ): NumberSelector(
                NumberSelectorConfig(
                    min=15, max=30, step=0.5, mode=NumberSelectorMode.SLIDER
                )
            ),
            vol.Required(
                CONF_TEMP_SETBACK,
                default=self.config_entry.data.get(CONF_TEMP_SETBACK, DEFAULT_TEMP_SETBACK),
            ): NumberSelector(
                NumberSelectorConfig(
                    min=15, max=30, step=0.5, mode=NumberSelectorMode.SLIDER
                )
            ),
        }
    )

    return self.async_show_form(step_id="init", data_schema=data_schema)
```