from eleclib.appliances.appliance import Appliance
from eleclib.utility import *

'''
##OVEN
###INTRO:
An Oven is a typical appliance in that it is easily defined by 
a running wattage and daily usage from which power and current
draw can be easily calculated.

###USAGE:
You can either initialize Oven without parameters and set the 
relevant values through the command prompt:
>myOven = Oven()
>myOven.prompt()

OR- You can pass values into the constructor directly. In this case
you should pass in **power_type, wattage, daily_usage**. with values 
defined in watts and hours respectively
>myOven = Oven("electric", 5000, 1)

Finally you can use its various reporting methods:
>print(str(myOven))
>myOven.get_consumption()

###TODO: 
* add prompt for usage- add this as an option in appliance
* add in support for electric-toaster @240V and electric @120V? (non-typical)
* scale down consumption to account for the oven not being at full draw
the whole time it is being used
'''

OVEN_TYPES = ["gas", "electric", "electric-toaster", "none"]
DEFAULT_OVEN_WATTAGE = 5000
OVEN_WATTAGE_RANGE = [1000,15000]
OVEN_USAGE_DAILY = 1

class Oven(Appliance):
    
    def __init__(self, power_type = OVEN_TYPES[0],
                 wattage=DEFAULT_OVEN_WATTAGE, 
                 daily_usage=OVEN_USAGE_DAILY,
                 house = None):
        
        super().__init__(DEFAULT_OVEN_WATTAGE,
                         OVEN_WATTAGE_RANGE,
                         'oven',
                         types = OVEN_TYPES, 
                         power_type = power_type,
                         wattage = wattage,
                         daily_usage = daily_usage,
                         b_prompt_usage = True)
        
    def get_consumption(self, days=1, peak=False):
        #actual wattage draw/rated wattage- self.wattage is the rated value
        usage_factor = 0.8
        return self.get_wattage()*self.get_usage()*days*usage_factor
