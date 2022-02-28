from eleclib.appliances.appliance import Appliance
from eleclib.utility import *

'''
##PUMP
###INTRO:
An Pump is a relatively typical appliance, but its daily_usage is
not usually known. Therefore we will calculate this value based on
the number of occupants in a household.

###USAGE:
You can either initialize Pump without parameters and set the 
relevant values through the command prompt:
>myPump = Pump()
>myPump.prompt()

OR- You can initialize it programatically as follows
>myPump = Pump(wattage=2500)
>myPump.set_usage(occupants=3)

Finally you can use its various reporting methods:
>print(str(myPump))
>myPump.get_consumption()

###TODO: 

'''

PUMP_TYPES = ["electric", "propane"]
DEFAULT_PUMP_WATTAGE = 2000 #1HP well pump
PUMP_WATTAGE_RANGE = [50, 15000]
DEFAULT_PUMP_USAGE = 1

class Pump(Appliance):
    
    def __init__(self, power_type = PUMP_TYPES[0],
                wattage=DEFAULT_PUMP_WATTAGE,
                daily_usage = None,
                house = None,
                occupants = None):
        
        if not house:
            self.occupants = occupants
            #else will be set by set_from_house
        super().__init__(DEFAULT_PUMP_WATTAGE,
                         PUMP_WATTAGE_RANGE,
                         'pump',
                         types = PUMP_TYPES, 
                         power_type = power_type,
                         wattage = wattage,
                         daily_usage = daily_usage,
                         house = house)
        
            
    def set_from_house(self, house):
        '''
        get occupants from house
        '''
        self.occupants = house.get_occupants()
        return True
        
    def set_usage(self, daily_usage=None):
        #set a specific usage (not usually known by user)
        if daily_usage:
            usage = daily_usage
        
        #set usage by number of occupants
        elif self.occupants:
            usage = 1 + 0.5*(self.occupants-1)
       
        #set default value
        else:
            usage = DEFAULT_PUMP_USAGE
        
        if super().set_usage(usage): return True
        return False