# Purpose
To create a python utility to simplify electrical and off-grid load calculations.\
Currently only the household load calculator is functional- see Module household

### This will eventually include:
* conductor sizing
* household load calculation
* solar, wind, and hydro considerations
* battery sizing
* pricing
* ... unfinished list ...

# Module household
You can create a Household object in order to call various accessors and reporter methods which for now only returns the total electrical load
## Getting Started
You can either create a new Household object programatically by supplying all or most inputs or by setting prompt=True and following the terminal prompts to set it up:

>from electriclib.household import Household\
>myHouse = Household(prompt=True)

### Household(self,**kwargs):

| param | default | description |
| :--- | :--- | :---
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

## Public Methods:

### get_peak_current():
Returns the peak current in Amps. This is often needed in sizing panels, main lines, and ogg grid components like batteries and fuses.

### get_power_usage():
Returns power usage in Killowatt hours. You can use this with peak=True and timespan=1, to get the peak daily value which is a useful number in calculating off grid requirements like battery capacity and power production from solar, wind, or hydro.

>myHouse.get_power_usage(1, peak=True)

| Inputs | Default | Required | Description
| :--- | :--- | :--- | :---
| timespan | 1 | True | Int- number of days. Defaults to a daily power usage (1) but can be set  to 30 to get monthly (typical billing cycle) or 365 for yearly power usage.
| peak | False | False | Bool- wether to give us the peak value (True) or the average. Default is the average. 

### get_recommendations():
Returns recommendations for reducing power consumption. It can suggest things like switching an appliance to 12V from 120V if it is more efficient (off-grid fridge).

### report():
Generates a report so that the info can be used and viewed later. Supports only the xlsx format at the moment.

| Inputs | Default | Required | Description
| :--- | :--- | :--- | :---
| file_path | "./report.xlsx" | True | String- File path for the generated report. Only supports xlsx at the moment.