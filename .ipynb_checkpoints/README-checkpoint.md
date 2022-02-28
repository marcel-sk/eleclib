# Purpose
To create a python utility to simplify electrical and off-grid load calculations.\
I find myself writing short scripts to run various calculations quite frequently and figured I should create something more versatile and reusable that could help others interested in off-grid power solutions!
Currently only the household load calculator is functional- see Module household

### This will eventually include:
* conductor sizing
* household load calculation
* solar, wind, and hydro considerations
* battery sizing
* pricing
* ... unfinished list ...

# Module household
## Class Household
You can create a Household object in order to call various accessors and reporter methods. The Household class will hold a list of appliances which will each contribute to the total load as well as information about the building, number of occupants and location.
### Getting Started
The easiest way to get started is to create a Household object without supplying any arguments and then populating the relevant values through interactive command prompts:
>from electriclib.household import Household\
>myHouse = Household()\
>myHouse.prompt_for_args()

Alternatively you can set it up programmatically, by supplying many or all of the input arguments (shown below), with the unsupplied arguments being set to default values. These inputs include a list of appliances which can be either a list of strings or Appliance type objects.

>myHouse = Household(square_footage = 4000,\ 
                    R_roof = 40,\
                    R_walls = 18,\ 
                    occupants = 4,\ 
                    appliances = ['oven', 'lights', 'pump'])

Finally the Household object can be used to get load information as follows:
>myHouse.get_consumption() #daily average in watts\
>myHouse.get_peak_current() #peak current (Amps)

These values can be used directly for determining the service size needed.

### __init__(self,**kwargs):

| param | default | description |
| :--- | :--- | :---
|square_footage|6000|Int- total household square footage
|R_roof|30|INT- 0 to 100 Average R-value of the roof default is from building code for Ontario as of 2021
|R_walls|24|INT- 0 to 100 Average R-value of the walls. default is from building code for Ontario as of 2021
|off_grid| False | Bool- is the house off-grid in the sense of not being connected to a municipal power grid.
|occupants|3|Int- 0 to 100. Number of permanent occupants. Used to determine water usage, lighting, etc.
|appliances|["heater", "water heater", "fridge", "lights", "pump", "oven"]|list of str or Apliance specifying which appliances are in the household.

### Public Methods:
**prompt_for_args()**  
Starts the command prompts to specify the Household parameters.

**get_peak_current()**  
Returns the peak current in Amps. This is often needed in sizing panels, main lines, and off grid components like batteries and fuses.

**get_power_consumption()**  
Returns power usage in watt hours. You can use this with peak=True and timespan=1, to get the peak daily value which is a useful number in calculating off grid requirements like battery capacity and power production from solar, wind, or hydro.

| Inputs | Default | Required | Description |
| :--- | :--- | :--- | :---
| days | 1 | False | Int- number of days. Defaults to a daily power usage (1) but can be set  to 30 to get monthly (typical billing cycle) or 365 for yearly power usage.
| peak | False | False | Bool- wether to give us the peak value (True) or the average. Default is the average. 

**get_recommendations()**  
Returns recommendations for reducing power consumption. It can suggest things like switching an appliance to 12V from 120V if it is more efficient (off-grid fridge).

**__str__()**  
Built-in str() function is implemented for Household as well as Appliances for convenient file or command-line display of current settings
>print(str(myHouse))

**report()**  
Generates a report so that the info can be used and viewed later. Supports only the xlsx and txt format at the moment.

| Inputs | Default | Required | Description |
| :--- | :--- | :--- | :---
| file_path | "./report.xlsx" | True | String- File path for the generated report. Only supports .xlsx and .txt at the moment.

### ...More
See appliances/README.md for details on Appliance classes and their use as standalones.

### TODO
* finish report() method
* implement docstrings and generate documentation
* use annotations consistently to make inputs more evident
* should I use args, and kwargs in appliances?
    this way I could look at what has been supplied and separate into concise constructor blocks...
