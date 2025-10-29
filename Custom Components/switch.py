“”“Switch platform for Dynamic Heating Scheduler.”””
from **future** import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import DynamicHeatingCoordinator

_LOGGER = logging.getLogger(**name**)

async def async_setup_entry(
hass: HomeAssistant,
entry: ConfigEntry,
async_add_entities: AddEntitiesCallback,
) -> None:
“”“Set up Dynamic Heating switches.”””
coordinator: DynamicHeatingCoordinator = hass.data[DOMAIN][entry.entry_id]

```
switches = [
    DynamicHeatingMasterSwitch(coordinator, entry),
]

async_add_entities(switches)
```

class DynamicHeatingMasterSwitch(CoordinatorEntity, SwitchEntity):
“”“Switch to enable/disable dynamic heating schedule.”””

```
_attr_icon = "mdi:thermostat-auto"
_attr_has_entity_name = True

def __init__(
    self,
    coordinator: DynamicHeatingCoordinator,
    entry: ConfigEntry,
) -> None:
    """Initialize the switch."""
    super().__init__(coordinator)
    self.entry = entry
    self._attr_unique_id = f"{entry.entry_id}_master_switch"
    self._attr_name = "Dynamic Heating Active"
    self._is_on = True

@property
def device_info(self) -> dict[str, Any]:
    """Return device information."""
    return {
        "identifiers": {(DOMAIN, self.entry.entry_id)},
        "name": self.entry.data[CONF_NAME],
        "manufacturer": "Dynamic Heating Scheduler",
        "model": "Heating Coordinator",
    }

@property
def is_on(self) -> bool:
    """Return true if switch is on."""
    return self._is_on

async def async_turn_on(self, **kwargs: Any) -> None:
    """Turn the switch on."""
    self._is_on = True
    self.async_write_ha_state()
    # Trigger immediate update
    await self.coordinator.async_refresh()

async def async_turn_off(self, **kwargs: Any) -> None:
    """Turn the switch off."""
    self._is_on = False
    self.async_write_ha_state()
```
