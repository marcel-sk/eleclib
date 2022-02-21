# Purpose
To create a python utility to simplify electrical load calculations.
### This will eventually include:
* conductor sizing
* household load calculation
* solar, wind, and hydro considerations
* battery sizing
* pricing
* ... unfinished list ...

# Module household
## Class Household
### Parameters(all optional):
|param|default|description
|*---*|*---*|---
|prompt|False|If True construct the Household through interactive command prompts
|square_footage|6000|Int- total household square footage
|heating_type|"gas"|String- ["gas","wood","baseboard-electric","geo-electric","infloor-electric","none"]
|water_heater_type|"gas"|String- ["gas","electric","none"]
|oven_type|"gas"|String- ["gas", "electric-full", "electric-toaster", "none"]
|oven_wattage|0|INT- 1000 to 5000
|fridge_type|"electric"|String- ["electric", "electic-low-volt", "propane", "propane-electric"]
|fridge_wattage|400|INT- 50 to 5000 in Kwh/year of usage
|light_bulbs|"LED"|String- ["LED", "halogen", "incandescent"]
|R_roof|30|INT- 0 to 100 Average R-value of the roof default is from building code for Ontario as of 2021
|R_walls|24|INT- 0 to 100 Average R-value of the walls. default is from building code for Ontario as of 2021
|occupants|3|Int- 0 to 100. Number of permanent occupants. Used to determine water usage, lighting, etc.

###Methods:
constructor
Intended use is either by\

house = Household(prompt=True)

or by specifying all known parameters with prompt=False\

house.get_powert_usage() returns watts per day consumption as an average of the yearly usage

