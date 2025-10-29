# Dynamic Heating Scheduler for Home Assistant

A custom Home Assistant integration that optimizes heating schedules based on dynamic energy prices. Automatically adjusts heating zones to boost when prices are low and setback when prices are high, with intelligent comfort hour management and COP optimization.

## Features

- **Universal Price Sensor Support**: Automatically detects and parses data from multiple energy price integrations:
  - Nordpool
  - Amber Electric
  - Octopus Energy
  - ENTSO-E
  - Tibber
  - aWATTar
  - Generic sensors with hourly forecasts
  
- **Intelligent 3-Tier Pricing**: Dynamically calculates low/normal/high price tiers based on daily price distribution

- **Multi-Zone Support**: Control unlimited heating zones independently

- **Comfort Hours**: Override price-based scheduling during specified hours

- **COP Optimization**: Pre-heat during low-price hours when outdoor temperatures are low for optimal heat pump efficiency

- **Home/Away Integration**: Automatically switch to away mode based on presence sensors

- **Min/Max Temperature Constraints**: Safety limits to prevent extreme temperatures

- **Manual Override**: Master switch to temporarily disable dynamic scheduling

## Installation

### HACS (Recommended)

1. Open HACS in Home Assistant
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/yourusername/dynamic_heating`
6. Category: Integration
7. Click "Add"
8. Search for "Dynamic Heating Scheduler"
9. Click "Download"
10. Restart Home Assistant

### Manual Installation

1. Download the `dynamic_heating` folder from this repository
2. Copy it to your `config/custom_components/` directory
3. Restart Home Assistant

## Configuration

### Initial Setup

1. Go to **Settings** → **Devices & Services**
2. Click **+ Add Integration**
3. Search for "Dynamic Heating Scheduler"
4. Follow the configuration steps:

#### Step 1: Basic Configuration
- **Integration Name**: Name for this heating setup
- **Energy Price Sensor**: Select your dynamic pricing sensor

#### Step 2: Global Settings
Configure your temperature preferences and optimization features:

- **Temperature Settings**:
  - **Boost Temperature**: Target when prices are low (e.g., 22°C)
  - **Normal Temperature**: Target during mid-range prices (e.g., 20°C)
  - **Setback Temperature**: Target when prices are high (e.g., 18°C)
  - **Away Temperature**: Target when nobody is home (e.g., 16°C)
  - **Min/Max Temperature**: Safety boundaries (e.g., 15-25°C)

- **Comfort Hours**:
  - **Start Time**: When comfort mode begins (e.g., 07:00)
  - **End Time**: When comfort mode ends (e.g., 23:00)
  - **Comfort Temperature**: Target during comfort hours (e.g., 21°C)

- **Optional Sensors**:
  - **Outdoor Temperature Sensor**: For COP optimization
  - **Home/Away Sensor**: For automatic away mode

- **COP Optimization**:
  - **Enable**: Turn on intelligent pre-heating
  - **Threshold**: Outdoor temp below which to boost heating (e.g., -5°C)

#### Step 3: Add Heating Zones
For each zone:
- **Zone Name**: Descriptive name (e.g., "Living Room")
- **Climate Entity**: Select the thermostat/climate entity

Repeat for all zones in your home.

## How It Works

### Price Tier Calculation

The integration analyzes the next 24 hours of price data and divides it into three tiers:

- **Low Tier**: Bottom third of price range (triggers boost heating)
- **Normal Tier**: Middle third (standard heating)
- **High Tier**: Top third (triggers setback heating)

### Decision Logic Priority

The system applies temperatures in this order:

1. **Away Mode** (highest priority): If away sensor is off
2. **Comfort Hours**: During specified comfort hours
3. **COP Optimization**: Pre-heat during low prices when outdoor temp is low
4. **Price Tier**: Standard low/normal/high tier temperatures
5. **Min/Max Constraints** (always enforced)

### Update Frequency

- **Hourly Updates**: Checks prices and adjusts plan every hour
- **5-Minute Checks**: Monitors current conditions and applies changes
- **Temperature Changes**: Only updates thermostats when change is ≥0.5°C

## Entities Created

### Sensors
- **Current Price Tier**: Shows current tier (low/normal/high)
- **Next Price Tier**: Shows upcoming tier change
- **Daily Low Price**: Lowest price in 24h forecast
- **Daily High Price**: Highest price in 24h forecast  
- **Daily Average Price**: Average price in 24h forecast

### Switches
- **Dynamic Heating Active**: Master on/off switch for the integration

### Attributes

The **Current Price Tier** sensor includes a `daily_plan` attribute with the full 24-hour schedule showing:
- Hour-by-hour price tiers
- Comfort hour flags
- COP boost flags
- Target temperatures

## Example Automations

### Notification on Tier Change

```yaml
automation:
  - alias: "Notify on High Price Period"
    trigger:
      - platform: state
        entity_id: sensor.dynamic_heating_current_price_tier
        to: "high"
    action:
      - service: notify.mobile_app
        data:
          message: "Heating entering high price period - temperatures reduced"
```

### Dashboard Card

```yaml
type: entities
title: Dynamic Heating
entities:
  - entity: switch.dynamic_heating_active
  - entity: sensor.dynamic_heating_current_price_tier
  - entity: sensor.dynamic_heating_next_price_tier
  - entity: sensor.dynamic_heating_daily_average_price
  - entity: sensor.dynamic_heating_daily_low_price
  - entity: sensor.dynamic_heating_daily_high_price
```

### Apex Charts Card (Price Visualization)

```yaml
type: custom:apexcharts-card
header:
  title: 24h Price Plan
series:
  - entity: sensor.dynamic_heating_current_price_tier
    data_generator: |
      return entity.attributes.daily_plan
        ? Object.entries(entity.attributes.daily_plan).map(([hour, data]) => {
            return [new Date(hour).getTime(), data.price];
          })
        : [];
```

## Supported Price Integrations

### Tested Integrations
- **Nordpool**: Native support
- **Octopus Energy**: Native support  
- **Tibber**: Native support
- **Amber Electric**: Native support

### Generic Support
If your integration isn't specifically supported, the integration will attempt to parse:
- `forecast` attributes with hourly price data
- `prices`, `hourly_prices`, or similar attributes
- Any sensor with timestamp + price pairs

## Troubleshooting

### Price sensor not recognized
Check the logs for parsing attempts. The integration tries multiple parsers and logs which one succeeds. If none work, you may need to add custom parsing logic.

### Temperatures not changing
1. Verify the master switch is ON
2. Check that climate entities are available
3. Ensure price sensor has valid forecast data
4. Check logs for errors

### COP optimization not working
1. Verify outdoor temperature sensor is configured
2. Check that COP optimization is enabled
3. Ensure outdoor temp is below the threshold
4. Verify price sensor shows low-tier hours

## Advanced Configuration

### Modifying Temperature Settings

Use the **Options** menu in the integration to adjust temperature targets without removing and re-adding the integration.

### Adding/Removing Zones

Currently requires removing and re-adding the integration. Zone management UI improvements are planned for future versions.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

### Adding Price Sensor Support

To add support for a new price integration, edit `price_parser.py` and add a new parser method following the existing pattern.

## Support

- GitHub Issues: Report bugs or request features
- Home Assistant Community: Discuss usage and share configurations

## License

MIT License - See LICENSE file for details

## Credits

Created for the Home Assistant community to help optimize heating costs with dynamic pricing.
