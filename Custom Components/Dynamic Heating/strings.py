{
“config”: {
“step”: {
“user”: {
“title”: “Dynamic Heating Scheduler”,
“description”: “Set up dynamic heating based on energy prices”,
“data”: {
“name”: “Integration Name”,
“price_sensor”: “Energy Price Sensor”
}
},
“global_settings”: {
“title”: “Global Heating Settings”,
“description”: “Configure temperature targets and comfort hours”,
“data”: {
“outdoor_temp_sensor”: “Outdoor Temperature Sensor (Optional)”,
“home_away_sensor”: “Home/Away Sensor (Optional)”,
“temp_boost”: “Boost Temperature (Low Price)”,
“temp_normal”: “Normal Temperature (Mid Price)”,
“temp_setback”: “Setback Temperature (High Price)”,
“temp_away”: “Away Mode Temperature”,
“temp_min”: “Minimum Temperature”,
“temp_max”: “Maximum Temperature”,
“comfort_start”: “Comfort Hours Start”,
“comfort_end”: “Comfort Hours End”,
“comfort_temp”: “Comfort Temperature”,
“enable_cop_optimization”: “Enable COP Optimization”,
“outdoor_temp_threshold”: “Outdoor Temp Threshold for COP Boost”
}
},
“zone_config”: {
“title”: “Add Heating Zone”,
“description”: “Configure a heating zone”,
“data”: {
“zone_name”: “Zone Name”,
“zone_climate”: “Climate Entity”
}
},
“add_zone”: {
“title”: “Add Another Zone?”,
“description”: “You have configured {zone_count} zone(s). Would you like to add another?”,
“data”: {
“add_another”: “Add Another Zone”
}
}
}
},
“entity”: {
“sensor”: {
“current_price_tier”: {
“name”: “Current Price Tier”
},
“next_price_tier”: {
“name”: “Next Price Tier”
},
“daily_low_price”: {
“name”: “Daily Low Price”
},
“daily_high_price”: {
“name”: “Daily High Price”
},
“daily_average_price”: {
“name”: “Daily Average Price”
}
},
“switch”: {
“dynamic_heating_active”: {
“name”: “Dynamic Heating Active”
}
}
}
}