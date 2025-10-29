“”“Sensor platform for Dynamic Heating Scheduler.”””
from **future** import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import (
ATTR_CURRENT_TIER,
ATTR_DAILY_PLAN,
ATTR_NEXT_TIER,
ATTR_NEXT_TIER_TIME,
ATTR_PRICE_AVERAGE,
ATTR_PRICE_HIGH,
ATTR_PRICE_LOW,
DOMAIN,
)
from .coordinator import DynamicHeatingCoordinator

_LOGGER = logging.getLogger(**name**)

async def async_setup_entry(
hass: HomeAssistant,
entry: ConfigEntry,
async_add_entities: AddEntitiesCallback,
) -> None:
“”“Set up Dynamic Heating sensors.”””
coordinator: DynamicHeatingCoordinator = hass.data[DOMAIN][entry.entry_id]

```
sensors = [
    DynamicHeatingCurrentTierSensor(coordinator, entry),
    DynamicHeatingNextTierSensor(coordinator, entry),
    DynamicHeatingPriceLowSensor(coordinator, entry),
    DynamicHeatingPriceHighSensor(coordinator, entry),
    DynamicHeatingPriceAverageSensor(coordinator, entry),
]

async_add_entities(sensors)
```

class DynamicHeatingSensorBase(CoordinatorEntity, SensorEntity):
“”“Base class for Dynamic Heating sensors.”””

```
def __init__(
    self,
    coordinator: DynamicHeatingCoordinator,
    entry: ConfigEntry,
) -> None:
    """Initialize the sensor."""
    super().__init__(coordinator)
    self.entry = entry
    self._attr_has_entity_name = True

@property
def device_info(self) -> dict[str, Any]:
    """Return device information."""
    return {
        "identifiers": {(DOMAIN, self.entry.entry_id)},
        "name": self.entry.data[CONF_NAME],
        "manufacturer": "Dynamic Heating Scheduler",
        "model": "Heating Coordinator",
    }
```

class DynamicHeatingCurrentTierSensor(DynamicHeatingSensorBase):
“”“Sensor showing current price tier.”””

```
_attr_icon = "mdi:cash-clock"

def __init__(
    self,
    coordinator: DynamicHeatingCoordinator,
    entry: ConfigEntry,
) -> None:
    """Initialize the sensor."""
    super().__init__(coordinator, entry)
    self._attr_unique_id = f"{entry.entry_id}_current_tier"
    self._attr_name = "Current Price Tier"

@property
def native_value(self) -> str | None:
    """Return the current price tier."""
    if not self.coordinator.data:
        return None
    return self.coordinator.data.get(ATTR_CURRENT_TIER)

@property
def extra_state_attributes(self) -> dict[str, Any]:
    """Return additional attributes."""
    if not self.coordinator.data:
        return {}

    return {
        ATTR_DAILY_PLAN: self.coordinator.data.get(ATTR_DAILY_PLAN, {}),
    }
```

class DynamicHeatingNextTierSensor(DynamicHeatingSensorBase):
“”“Sensor showing next price tier.”””

```
_attr_icon = "mdi:clock-outline"

def __init__(
    self,
    coordinator: DynamicHeatingCoordinator,
    entry: ConfigEntry,
) -> None:
    """Initialize the sensor."""
    super().__init__(coordinator, entry)
    self._attr_unique_id = f"{entry.entry_id}_next_tier"
    self._attr_name = "Next Price Tier"

@property
def native_value(self) -> str | None:
    """Return the next price tier."""
    if not self.coordinator.data:
        return None
    return self.coordinator.data.get(ATTR_NEXT_TIER)

@property
def extra_state_attributes(self) -> dict[str, Any]:
    """Return additional attributes."""
    if not self.coordinator.data:
        return {}

    next_time = self.coordinator.data.get(ATTR_NEXT_TIER_TIME)
    return {
        ATTR_NEXT_TIER_TIME: next_time.isoformat() if next_time else None,
    }
```

class DynamicHeatingPriceLowSensor(DynamicHeatingSensorBase):
“”“Sensor showing lowest price of the day.”””

```
_attr_icon = "mdi:cash-minus"
_attr_native_unit_of_measurement = "currency/kWh"

def __init__(
    self,
    coordinator: DynamicHeatingCoordinator,
    entry: ConfigEntry,
) -> None:
    """Initialize the sensor."""
    super().__init__(coordinator, entry)
    self._attr_unique_id = f"{entry.entry_id}_price_low"
    self._attr_name = "Daily Low Price"

@property
def native_value(self) -> float | None:
    """Return the lowest price."""
    if not self.coordinator.data:
        return None
    return self.coordinator.data.get(ATTR_PRICE_LOW)
```

class DynamicHeatingPriceHighSensor(DynamicHeatingSensorBase):
“”“Sensor showing highest price of the day.”””

```
_attr_icon = "mdi:cash-plus"
_attr_native_unit_of_measurement = "currency/kWh"

def __init__(
    self,
    coordinator: DynamicHeatingCoordinator,
    entry: ConfigEntry,
) -> None:
    """Initialize the sensor."""
    super().__init__(coordinator, entry)
    self._attr_unique_id = f"{entry.entry_id}_price_high"
    self._attr_name = "Daily High Price"

@property
def native_value(self) -> float | None:
    """Return the highest price."""
    if not self.coordinator.data:
        return None
    return self.coordinator.data.get(ATTR_PRICE_HIGH)
```

class DynamicHeatingPriceAverageSensor(DynamicHeatingSensorBase):
“”“Sensor showing average price of the day.”””

```
_attr_icon = "mdi:cash"
_attr_native_unit_of_measurement = "currency/kWh"

def __init__(
    self,
    coordinator: DynamicHeatingCoordinator,
    entry: ConfigEntry,
) -> None:
    """Initialize the sensor."""
    super().__init__(coordinator, entry)
    self._attr_unique_id = f"{entry.entry_id}_price_average"
    self._attr_name = "Daily Average Price"

@property
def native_value(self) -> float | None:
    """Return the average price."""
    if not self.coordinator.data:
        return None
    return self.coordinator.data.get(ATTR_PRICE_AVERAGE)
```