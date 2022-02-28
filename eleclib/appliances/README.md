# Purpose
This set of modules is intended to be used internally, however flexibility has been built in so each class can be used as a standalone for calculating consumption or current draw.

# Class Appliance:

An **appliances.Appliance** defines an appliance by name, power types, wattage range, and default wattage. Methods common to all appliances are shown below.
These values in turn let us calculate its contribution to total
current draw and power consumption for a Household. See child classes *UsageAppliance* and *HouseholdAppliance* for more details.

### USAGE:
**Do not use Appliance directly**- see individual appliances like Oven, Pump...
As with the Household class there are two main ways of using an Appliance. First is to initialize it without parameters (or with only household- see HouseholdAppliance):
>myHouse = Household(...)\
>myHeater = Heater(household=myHouse)\
>myHeater.prompt()
>print(str(myHeater))\
>consumption = myHeater.get_consumption()\

The second method is to set it up programmatically by providing the inputs specific to the subclass:
>myFridge = Fridge(wattage=350, unit='kwh/yr')


### Public Methods:

**get_peak_current()**  
Like the Household method. It returns the peak current in Amps. 

| Inputs | Default | Required | Description |
| :--- | :--- | :--- | :---
| standalone | False | False | Bool- if True this will get the instantaneous maximum value. Otherwise it will return the value that would be used in overall load calculations which is lower for appliances that have a startup spike.

**get_consumption()**  
Like the Household method. It returns the power consumption in watt hours.

| Inputs | Default | Required | Description
| :--- | :--- | :--- | :---
| days | 1 | False | Int- number of days over which to calculate the consumption
| peak | False | False | Bool- if True this will return the maximum value. For some appliances like Heaters this will be much different than the average, for others like a pump it should not change year round.

**prompt()**  
Starts the command prompt to set the relevant parameters like wattage, type, etc.

**__str__()**  
generates a (multiline) string representation of the appliance
>str(Appliance)

**is_electric()**  
Returns bool type defining wether or not the appliance is powered by electricity.

# Class UsageAppliance(Appliance):

An **appliances.UsageAppliance** defines appliances which are most easily defined by their wattage and usage. Appliances like Oven(s) are easily defined as such while others like Pump(s) do not typically have a known number of running hours per day.

Note: no aditional public methods defined beyond Appliance methods.

### Includes:
* Oven
* Fridge

### USAGE:
>myOven = Oven()\
>myOven.prompt()

OR
>myOven = Oven(wattage=4000, usage=1.5)

Finally
>consumption = myOven.get_consumption()
>peak_current = myOven.get_peak_current()

# Class HouseholdAppliance(Appliance):

An **appliance.HouseholdAppliance** is an **internal type**. It defines appliances that rely on information from our Household definition. This includes values like square footage, insulation, and number of occupants. To set the relevant household paramteres you can either pass in a Household object to the constructor or set the values one at a time through the command prompt.

### USAGE:
As for all appliances the appliance-specific data can be either passed in directly or set up by calling prompt(). If a Household is supplied the household-specific parameters will not be prompted.

>myHeater = Heater(household=myHouse)\
>myHeater.prompt()

OR
>myHeater = Heater(square_footage=4000,R_roof=30,R_walls=20, wattage=5000)

### Includes:
* Heater
* WaterHeater
* Lights
* Pump  

# Class Oven(UsageAppliance)
An Oven is a typical appliance in that it is easily defined by 
a running wattage and daily usage from which power and current
draw can be easily calculated.

### USAGE:

>myOven = Oven("electric", 5000, 1)

OR
>myOven = Oven()
>myOven.prompt()

### __init__(self,**kwargs):

| param | default | description |
| :--- | :--- | :---
|type|'electric'|Str- one of ['electric', 'electric-toaster', 'gas', 'propane']
|wattage|5000|INT- Running wattage for the oven
|usage|1|INT- number of average running hours per day


### TODO: 
* add in support for electric-toaster @240V and electric @120V? (non-typical)
* scale down consumption to account for the oven not being at full draw the whole time it is being used


# Class Fridge(UsageAppliance)
A fridge typically consumes a stable amount of power year round. 
Its power will be known in terms of kwh/yr or sometimes running watts (less
precise). In the case of watts we can use daily_usage to 
find the kwh/yr value. This value is the actual running time of the
fridge compressor in hours per day.

### USAGE

>myFridge = Fridge('electric', 400, unit='kwh/yr')

OR
>myFridge = Fridge()
>myFridge.prompt()

### __init__(self,**kwargs):

| param | default | description |
| :--- | :--- | :--- 
|power_type|'electric'|Str- one of ['electric', 'propane']
|wattage|5000|INT- Running wattage for the oven
|usage|1|INT- number of average running hours per day
|unit|'watts'|

### TODO: 
* add support for propane-electric which may be run on propane part of the year and electric the rest.

# Class Heater(HouseholdAppliance)
A HEATER varies greatly in output based on environmental conditions.
As such defining wattage of an electrical heater is only relevant for 
the purpose of calculating current draw, while power consumption is
related to the efficiency of the heater, the temperature outside and 
the building structure.

### USAGE:

>myHeater = Heater('electric', 4000, household=myHouse)

OR
>myHeater = Heater('electric', 4000,
                    square_footage=6000,
                    R_roof = 30,
                    R_walls = 24)
                    
OR
>myHeater = Heater()  
>myHeater.prompt()
                    
### __init__(self,**kwargs):

| param | default | description |
| :--- | :--- | :--- 
|power_type|'electric'|Str- one of ['electric', 'gas', 'propane']
|wattage|4000|INT- Running wattage for the heater
|square_footage|6000|INT- square footage of the house
|R_roof|30|float- Insulation R-value for the roof/attic of the house
|R_walls|24|float- Insulation R-value for the walls of the house
|household|None|Household- overrides square_footage and R-values with Household params


### TODO: 
* support for seasonal changes- see get_consumption args
* perfect the get_consumption calculations
* add efficiency to prompt

# Class Lights
Lights will typically produce a relatively stable power consumption 
year round. The amount will typically be dependant on size of a house, 
number of occupants, and type of bulbs used. Since we are treating 
all the lights in a house as a single appliance it makes sense to define
wattage as the average value and use a 24-hour usage to calculate 
consumption.

### USAGE:
You can either initialize Lights without parameters and set the 
relevant values through the command prompt:
>myLights = Lights('halogen', 4, 6000)

OR
>myLights = Lights('LED', household=myHouse)

OR
>myLights = Lights()  
>myLights.prompt()

### __init__(self,**kwargs):

| param | default | description |
| :--- | :--- | :--- 
|bulb_type|'LED'|Str- one of ['LED', 'halogen', 'incandescent']
|occupants|3|INT- number of people living in the house
|square_footage|6000|INT- square footage of the house
|household|None|Household- overrides occupants and square_footage with Household parameters

### TODO: 
* support different default wattages for diferent bulbs
* add all bulb types

# Class WaterHeater(HouseholdAppliance)
An WaterHeater (if electric) will have a known wattage, but the daily_usage 
will be defined by the number of occupants in a Household- much like the Pump
class.

### USAGE:
You can either initialize WaterHeater without parameters and set the 
relevant values through the command prompt:
>myWaterHeater = WaterHeater('electric', 4000, 4)

OR
>myWaterHeater = WaterHeater('electric', 5000, household=myHouse)

OR
>myWaterHeater = WaterHeater()  
>myWaterHeater.prompt()

### __init__(self,**kwargs):

| param | default | description |
| :--- | :--- | :--- 
|power_type|'electric'|Str- one of ['electric', 'propane']
|wattage|4000|Int- running wattage of the water heater
|occupants|3|INT- number of people living in the house
|household|None|Household- overrides occupants with Household parameter

### TODO: 
* add water heater capacity to the calculations

# Class Pump(HouseholdAppliance)
An Pump will have a known wattage, but its usage (running hours per day) will be determined by only the number of occupants living in the house.

### USAGE:

>myPump = Pump('electric', 4000, 4)

OR
>myPump = Pump('electric', 2500, household=myHouse)

OR
>myPump = Pump()  
>myPump.prompt()

### __init__(self,**kwargs):

| param | default | description |
| :--- | :--- | :--- 
|power_type|'electric'|Str- one of ['electric', 'electric-low-volt', 'propane']
|wattage|4000|Int- running wattage of the pump
|occupants|3|INT- number of people living in the house
|household|None|Household- overrides occupants with Household parameter

### TODO: 
* allow wattage to be set by well depth, horsepower