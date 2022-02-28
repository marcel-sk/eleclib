from eleclib.appliances.appliance import Appliance
from eleclib.utility import *
from numbers import Number
'''
##WATER HEATER
###INTRO:
An WaterHeater (if electric) will have a known wattage, but the daily_usage 
will be defined by the number of occupants in a Household- much like the Pump
class.

###USAGE:
You can either initialize WaterHeater without parameters and set the 
relevant values through the command prompt:
>myWaterHeater = WaterHeater()
>myWaterHeater.prompt()

OR- You can define it programatically by providing **wattage** AND
either **occupants** OR **daily_usage** OR **house** where daily_usage
is pump running time in hours, and house is of type Household
>myhouse = Household()
>myWaterHeater = WaterHeater(wattage=4000, house= myHouse)

Finally you can use its various reporting methods:
>print(str(myWaterHeater))
>myWaterHeater.get_consumption()

###TODO: 

'''
WATER_HEATER_TYPES = ["gas","electric","none"]
DEFAULT_WATER_HEATER_WATTAGE = 4000
WATER_HEATER_WATTAGE_RANGE = [500,10000]
DEFAULT_WATER_HEATER_CAP = 50 #Gallons
WATER_HEATER_CAPACITY_RANGE = [3,200]
WATER_HEATER_USAGE_DAILY = 3

class WaterHeater(Appliance):
    
    def __init__(self, power_type = WATER_HEATER_TYPES[0],
                 wattage = DEFAULT_WATER_HEATER_WATTAGE, 
                 daily_usage = WATER_HEATER_USAGE_DAILY,
                 occupants = None,
                 house = None):
        
        if not house:
            self.occupants = occupants
            
        super().__init__(DEFAULT_WATER_HEATER_WATTAGE,
                         WATER_HEATER_WATTAGE_RANGE,
                         'water heater',
                         types = WATER_HEATER_TYPES, 
                         power_type = power_type,
                         wattage = wattage,
                         daily_usage = daily_usage,
                         house = house)
        
        self.default_capacity = DEFAULT_WATER_HEATER_CAP
        self.capacity_range = WATER_HEATER_CAPACITY_RANGE
       
            
    def set_from_house(self, house):
        '''
        get occupants from house
        '''
        self.occupants = house.get_occupants()
        return True
    
    def set_capacity(self, capacity):
        assert(isinstance(capacity,Number))
        if self.capacity_range[0] <= capacity <= self.capacity_range[1]:
            self.capacity = capacity
            return True
        return False
        
    
    def set_usage(self, daily_usage=None):
        #set a specific usage (not usually known by user)
        if daily_usage:
            usage = daily_usage
        
        #set usage by number of occupants and heater size
        elif self.occupants:
            running_time = 2 + self.occupants
            usage = running_time*self.wattage
            
        #set default value
        else:
            usage = WATER_HEATER_USAGE_DAILY
        
        if super().set_usage(usage): return True
        return False
    
    def prompt(self, get_input=input):
        self.prompt_type(get_input)
        if self.is_electric():
            self.prompt_wattage(get_input)
            self.prompt_capacity(get_input)
            
    def prompt_capacity(self, get_input=input):
        capacity_raw = get_input("enter " + self.name + " capacity (default: " + str(self.default_capacity) + ") >")
        #no entry, use default
        if not capacity_raw:
            if self.set_capacity(self.default_capacity):
                return True
            return False
                      
        else:
            capacity = extract_number(capacity_raw)
            if capacity and self.set_capacity(capacity):
                return True
            else:
                print("Error: Input invalid!")
                min_val = self.capacity_range[0]
                max_val = self.capacity_range[1]
                print("should be an integer between ", min_val, " and ", max_val, " representing the water heater capacity in gallons")
                self.prompt_capacity(get_input)