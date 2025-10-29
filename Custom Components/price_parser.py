“”“Price parser for multiple energy price integrations.”””
from **future** import annotations

import logging
from datetime import datetime, timedelta
from typing import Any

from homeassistant.core import HomeAssistant, State
from homeassistant.util import dt as dt_util

_LOGGER = logging.getLogger(**name**)

class PriceParser:
“”“Parse price data from various Home Assistant integrations.”””

```
def __init__(self, hass: HomeAssistant) -> None:
    """Initialize the price parser."""
    self.hass = hass

async def parse_price_sensor(self, state: State) -> list[dict[str, Any]]:
    """Parse price sensor and return hourly prices for next 24 hours."""
    # Try different parsing methods based on integration type
    parsers = [
        self._parse_nordpool,
        self._parse_amber,
        self._parse_octopus,
        self._parse_entsoe,
        self._parse_tibber,
        self._parse_awattar,
        self._parse_generic_forecast,
        self._parse_generic_attributes,
    ]

    for parser in parsers:
        try:
            result = await parser(state)
            if result:
                _LOGGER.debug(
                    "Successfully parsed prices using %s", parser.__name__
                )
                return result
        except Exception as err:
            _LOGGER.debug("Parser %s failed: %s", parser.__name__, err)
            continue

    _LOGGER.warning(
        "Could not parse price data from sensor %s. "
        "Integration may not be supported or data format unknown.",
        state.entity_id,
    )
    return []

async def _parse_nordpool(self, state: State) -> list[dict[str, Any]] | None:
    """Parse Nordpool integration sensor."""
    if "nordpool" not in state.entity_id.lower():
        return None

    prices = []
    attributes = state.attributes

    # Nordpool stores prices in 'raw_today' and 'raw_tomorrow' attributes
    today = attributes.get("raw_today", [])
    tomorrow = attributes.get("raw_tomorrow", [])

    now = dt_util.now()
    current_hour = now.replace(minute=0, second=0, microsecond=0)

    for entry in today + tomorrow:
        if isinstance(entry, dict):
            start_time = entry.get("start")
            price = entry.get("value")

            if start_time and price is not None:
                if isinstance(start_time, str):
                    start_time = dt_util.parse_datetime(start_time)

                if start_time and start_time >= current_hour:
                    prices.append({"hour": start_time, "price": float(price)})

    return prices[:24] if prices else None

async def _parse_amber(self, state: State) -> list[dict[str, Any]] | None:
    """Parse Amber Electric integration sensor."""
    if "amber" not in state.entity_id.lower():
        return None

    attributes = state.attributes
    forecasts = attributes.get("forecasts", [])

    if not forecasts:
        return None

    prices = []
    now = dt_util.now()
    current_hour = now.replace(minute=0, second=0, microsecond=0)

    for forecast in forecasts:
        start_time = forecast.get("start_time")
        price = forecast.get("per_kwh")

        if start_time and price is not None:
            if isinstance(start_time, str):
                start_time = dt_util.parse_datetime(start_time)

            if start_time and start_time >= current_hour:
                prices.append({"hour": start_time, "price": float(price)})

    return prices[:24] if prices else None

async def _parse_octopus(self, state: State) -> list[dict[str, Any]] | None:
    """Parse Octopus Energy integration sensor."""
    if "octopus" not in state.entity_id.lower():
        return None

    attributes = state.attributes
    rates = attributes.get("rates", [])

    if not rates:
        return None

    prices = []
    now = dt_util.now()
    current_hour = now.replace(minute=0, second=0, microsecond=0)

    for rate in rates:
        start_time = rate.get("start") or rate.get("valid_from")
        price = rate.get("value_inc_vat") or rate.get("value")

        if start_time and price is not None:
            if isinstance(start_time, str):
                start_time = dt_util.parse_datetime(start_time)

            if start_time and start_time >= current_hour:
                prices.append({"hour": start_time, "price": float(price)})

    return prices[:24] if prices else None

async def _parse_entsoe(self, state: State) -> list[dict[str, Any]] | None:
    """Parse ENTSO-E integration sensor."""
    if "entsoe" not in state.entity_id.lower():
        return None

    attributes = state.attributes
    prices_raw = attributes.get("prices", {})

    if not prices_raw:
        return None

    prices = []
    now = dt_util.now()
    current_hour = now.replace(minute=0, second=0, microsecond=0)

    for timestamp_str, price in prices_raw.items():
        try:
            timestamp = dt_util.parse_datetime(timestamp_str)
            if timestamp and timestamp >= current_hour:
                prices.append({"hour": timestamp, "price": float(price)})
        except (ValueError, TypeError):
            continue

    return sorted(prices, key=lambda x: x["hour"])[:24] if prices else None

async def _parse_tibber(self, state: State) -> list[dict[str, Any]] | None:
    """Parse Tibber integration sensor."""
    if "tibber" not in state.entity_id.lower():
        return None

    attributes = state.attributes
    today = attributes.get("today", [])
    tomorrow = attributes.get("tomorrow", [])

    all_prices = today + tomorrow

    if not all_prices:
        return None

    prices = []
    now = dt_util.now()
    current_hour = now.replace(minute=0, second=0, microsecond=0)

    for entry in all_prices:
        start_time = entry.get("startsAt")
        price = entry.get("total")

        if start_time and price is not None:
            if isinstance(start_time, str):
                start_time = dt_util.parse_datetime(start_time)

            if start_time and start_time >= current_hour:
                prices.append({"hour": start_time, "price": float(price)})

    return prices[:24] if prices else None

async def _parse_awattar(self, state: State) -> list[dict[str, Any]] | None:
    """Parse aWATTar integration sensor."""
    if "awattar" not in state.entity_id.lower():
        return None

    attributes = state.attributes
    data = attributes.get("data", [])

    if not data:
        return None

    prices = []
    now = dt_util.now()
    current_hour = now.replace(minute=0, second=0, microsecond=0)

    for entry in data:
        start_time = entry.get("start_timestamp")
        price = entry.get("marketprice")

        if start_time and price is not None:
            # aWATTar uses Unix timestamps
            if isinstance(start_time, (int, float)):
                start_time = dt_util.utc_from_timestamp(start_time / 1000)
            elif isinstance(start_time, str):
                start_time = dt_util.parse_datetime(start_time)

            if start_time and start_time >= current_hour:
                prices.append({"hour": start_time, "price": float(price)})

    return prices[:24] if prices else None

async def _parse_generic_forecast(self, state: State) -> list[dict[str, Any]] | None:
    """Parse generic sensor with forecast attribute."""
    attributes = state.attributes
    forecast = attributes.get("forecast")

    if not forecast or not isinstance(forecast, list):
        return None

    prices = []
    now = dt_util.now()
    current_hour = now.replace(minute=0, second=0, microsecond=0)

    for entry in forecast:
        # Try various timestamp field names
        start_time = (
            entry.get("datetime")
            or entry.get("timestamp")
            or entry.get("start")
            or entry.get("time")
        )

        # Try various price field names
        price = (
            entry.get("price")
            or entry.get("value")
            or entry.get("amount")
            or entry.get("rate")
        )

        if start_time and price is not None:
            if isinstance(start_time, str):
                start_time = dt_util.parse_datetime(start_time)

            if start_time and start_time >= current_hour:
                prices.append({"hour": start_time, "price": float(price)})

    return prices[:24] if prices else None

async def _parse_generic_attributes(self, state: State) -> list[dict[str, Any]] | None:
    """Parse generic sensor by scanning all attributes for price-like data."""
    attributes = state.attributes
    prices = []
    now = dt_util.now()
    current_hour = now.replace(minute=0, second=0, microsecond=0)

    # Look for attributes that might contain hourly prices
    price_attrs = [
        "prices",
        "hourly_prices",
        "price_data",
        "energy_prices",
        "electricity_prices",
    ]

    for attr_name in price_attrs:
        data = attributes.get(attr_name)
        if not data:
            continue

        if isinstance(data, dict):
            # Handle dict with timestamps as keys
            for timestamp_str, price in data.items():
                try:
                    timestamp = dt_util.parse_datetime(timestamp_str)
                    if timestamp and timestamp >= current_hour:
                        prices.append({"hour": timestamp, "price": float(price)})
                except (ValueError, TypeError):
                    continue

        elif isinstance(data, list):
            # Handle list of price objects
            for entry in data:
                if not isinstance(entry, dict):
                    continue

                start_time = None
                price = None

                # Try to find timestamp field
                for time_field in ["datetime", "timestamp", "start", "time", "hour"]:
                    if time_field in entry:
                        start_time = entry[time_field]
                        break

                # Try to find price field
                for price_field in ["price", "value", "amount", "rate", "cost"]:
                    if price_field in entry:
                        price = entry[price_field]
                        break

                if start_time and price is not None:
                    if isinstance(start_time, str):
                        start_time = dt_util.parse_datetime(start_time)

                    if start_time and start_time >= current_hour:
                        prices.append({"hour": start_time, "price": float(price)})

    if prices:
        return sorted(prices, key=lambda x: x["hour"])[:24]

    # If we still don't have prices, try to generate from current state
    # assuming hourly changes (fallback for very simple sensors)
    try:
        current_price = float(state.state)
        # Generate 24 hours with current price (not ideal, but better than nothing)
        for i in range(24):
            hour = current_hour + timedelta(hours=i)
            prices.append({"hour": hour, "price": current_price})
        
        _LOGGER.warning(
            "Using current price %.2f for all 24 hours (no forecast data found)",
            current_price,
        )
        return prices
    except (ValueError, TypeError):
        pass

    return None
```
