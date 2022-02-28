from eleclib.appliances.appliance import Appliance
from eleclib.utility import *
'''
##FRIDGE
###INTRO
A fridge typically consumes a stable amount of power year round. 
Its power will be known in terms of kwh/yr or sometimes running watts (less
precise). In the case of watts we can use daily_usage to 
find the kwh/yr value. This value is the actual running time of the
fridge compressor in hours per day.

###USAGE
You can either initialize a Fridge without parameters and set the 
relevant values through the command prompt:
>myFridge = Fridge()
>myFridge.prompt()

OR- You can pass values into the constructor directly.
>myFridge = Fridge(type = 'electric', wattage = 400, unit = 'kwh/yr')

Finally you can use its various reporting methods:
>print(str(myFridge))
>myFridge.get_consumption()

###TODO: 
* add support for propane-electric which may be run on propane part of 
the year and electric the rest.
'''

FRIDGE_TYPES = ["electric", "electic-low-volt", "propane", "propane-electric"]
DEFAULT_FRIDGE_WATTAGE_SPEC = "Kwh/yr"
WATTAGE_SPECS = ["Kwh/yr", "wh/day", "kwh/month", "running watts", "peak watts"]
#--THESE ARE IN KWH/YEAR--
DEFAULT_FRIDGE_WATTAGE = 400 #in kwh/yr
DEFAULT_12V_FRIDGE_WATTAGE = 250
FRIDGE_WATTAGE_RANGE = [50,5000]
FRIDGE_USAGE_DAILY = 8
#units that can be supplied and alternative ways of writing them
UNITS = {'kwh/yr': ['kwh/yr', 'kwh/year', 'kilowatt-hour/year', 'kilowatt hour per year', 'kilowatt-hour per year'],
         'watts': ['watts', 'watt', 'w'],
         'watts/day': ['watts/day', 'w/d', 'watt/day', 'watt/d', 'watts/d', 'w/day']}

class Fridge(Appliance):

    def __init__(self, power_type = FRIDGE_TYPES[0] ,
                 wattage = DEFAULT_FRIDGE_WATTAGE, 
                 unit = 'kwh/yr',
                 daily_usage = FRIDGE_USAGE_DAILY,
                 house = None):
        
        super().__init__(DEFAULT_FRIDGE_WATTAGE,
                        FRIDGE_WATTAGE_RANGE,
                        'fridge',
                        types = FRIDGE_TYPES, 
                        power_type = power_type,
                        daily_usage = daily_usage)
    
        if not self.set_wattage(wattage, unit):
            raise ValueError("invalid wattage/unit combination in Fridge constructor")
            
    def set_wattage(self, wattage= None, unit='watts'):
        
        if not wattage:
            if super().set_wattage(): return True
            
        else:
            assert(type(unit) == str)
            unit = unit.lower()
            if unit in UNITS['kwh/yr']:
                if super().set_wattage(wattage): return True
            elif unit in UNITS['watts/day']:
                if super().set_wattage(wattage*365/1000): return True
            elif unit in UNITS['watts']:
                if super().set_wattage(wattage*365*self.get_usage()/1000): return True
        return False
    
    def get_wattage(self, unit='watts'):
        assert(type(unit)==str)
        unit = unit.lower()
        if unit in UNITS['kwh/yr']:
            return int(self.wattage)
        elif unit in UNITS['watts/day']:
            return int(self.wattage*1000/365)
        elif unit in UNITS['watts']:
            return int(self.wattage*1000/(365*self.get_usage()))
        else:
            raise ValueError("Error: invalid unit supplied to get_wattage")
        return False
    
    def prompt_wattage(self, get_input):
        wattage_raw = get_input("enter fridge wattage (default: " + str(self.default_wattage) + " kwh/yr) >")
        #no entry, use default
        if not wattage_raw:
            assert(self.is_electric())
            if self.set_wattage(self.default_wattage):
                return True
            return False
                      
        else:
            wattage = extract_number(wattage_raw)
            if wattage and 'watts' in wattage_raw:
                if self.set_wattage(wattage):
                    return True
            elif wattage:
                if self.set_wattage(wattage, unit='kwh/yr'):
                    return True
            
        print("Error: Input invalid!")
        min_val = self.wattage_range[0]
        max_val = self.wattage_range[1]
        print("should be an integer between ", min_val, " and ", max_val, " representing the rated power in kwh/yr, OR a number followed by \'watts\' for running power")
        self.prompt_wattage(get_input)
    