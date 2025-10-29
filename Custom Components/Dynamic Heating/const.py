“”“Constants for Dynamic Heating Scheduler.”””

DOMAIN = “dynamic_heating”

# Config flow constants

CONF_ZONES = “zones”
CONF_ZONE_NAME = “zone_name”
CONF_ZONE_CLIMATE = “zone_climate”
CONF_PRICE_SENSOR = “price_sensor”
CONF_OUTDOOR_TEMP_SENSOR = “outdoor_temp_sensor”
CONF_HOME_AWAY_SENSOR = “home_away_sensor”

# Temperature settings

CONF_TEMP_BOOST = “temp_boost”
CONF_TEMP_NORMAL = “temp_normal”
CONF_TEMP_SETBACK = “temp_setback”
CONF_TEMP_AWAY = “temp_away”
CONF_TEMP_MIN = “temp_min”
CONF_TEMP_MAX = “temp_max”

# Comfort hours

CONF_COMFORT_START = “comfort_start”
CONF_COMFORT_END = “comfort_end”
CONF_COMFORT_TEMP = “comfort_temp”

# COP optimization

CONF_OUTDOOR_TEMP_THRESHOLD = “outdoor_temp_threshold”
CONF_ENABLE_COP_OPTIMIZATION = “enable_cop_optimization”

# Price tier settings

PRICE_TIER_LOW = “low”
PRICE_TIER_NORMAL = “normal”
PRICE_TIER_HIGH = “high”

# Default values

DEFAULT_TEMP_BOOST = 22
DEFAULT_TEMP_NORMAL = 20
DEFAULT_TEMP_SETBACK = 18
DEFAULT_TEMP_AWAY = 16
DEFAULT_TEMP_MIN = 15
DEFAULT_TEMP_MAX = 25
DEFAULT_COMFORT_START = “07:00”
DEFAULT_COMFORT_END = “23:00”
DEFAULT_COMFORT_TEMP = 21
DEFAULT_OUTDOOR_TEMP_THRESHOLD = -5
DEFAULT_ENABLE_COP_OPTIMIZATION = True

# Attributes

ATTR_CURRENT_TIER = “current_tier”
ATTR_NEXT_TIER = “next_tier”
ATTR_NEXT_TIER_TIME = “next_tier_time”
ATTR_DAILY_PLAN = “daily_plan”
ATTR_PRICE_LOW = “price_low”
ATTR_PRICE_HIGH = “price_high”
ATTR_PRICE_AVERAGE = “price_average”