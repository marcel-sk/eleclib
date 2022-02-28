from eleclib.appliances.appliance import Appliance
from eleclib.utility import *

'''
##HEATER
###INTRO:
Lights will typically produce a relatively stable power consumption 
year round. The amount will typically be dependant on size of a house, 
number of occupants, and type of bulbs used. Since we are treating 
all the lights in a house as a single appliance it makes sense to define
wattage as the average value and use a 24-hour usage to calculate 
consumption.

###USAGE:
You can either initialize Lights without parameters and set the 
relevant values through the command prompt:
>myLights = Lights()
>myLights.prompt()

OR- You can pass values into the constructor directly. In this case
you should pass in at least **square_footage, occupants**
OR **house** where the wattage is a 24-hour average value, and house
is a Household type object.
>myHouse = Household()
>myLights = Lights(house= myHouse)

Finally you can use its various reporting methods:
>print(str(myLights))
>myLights.get_consumption()

###TODO: 
* support different default wattages for diferent bulbs
'''

LIGHT_BULB_TYPES = ["LED", "halogen", "incandescent"]
DEFAULT_LIGHT_WATTAGE = 15
LIGHT_WATTAGE_RANGE = [0,10000]

class Lights(Appliance):
    
    def __init__(self, bulb_type = LIGHT_BULB_TYPES[0],
                wattage = DEFAULT_LIGHT_WATTAGE,
                square_footage = None,
                occupants = None,
                house = None):
        
        super().__init__(DEFAULT_LIGHT_WATTAGE,
                         LIGHT_WATTAGE_RANGE,
                         'lights',
                         types = ['electric'], 
                         wattage = wattage,
                         daily_usage = 24,
                         house = house)
        
        self.bulb_type = bulb_type
        self.bulb_types = LIGHT_BULB_TYPES
        
        #if house is supplied it super will call sest_from_house instead
        if not house:
            self.occupants = occupants
            self.square_footage = square_footage
        
        
    def set_from_house(self, house):
        '''
        get square_footage and occupants from house
        '''
        self.square_footage = house.get_square_footage()
        self.occupants = house.get_occupants()
        return True
            
    def __str__(self):
        text = "bulb type: " + self.bulb_type + "\n"
        return text
        
    def set_bulb_type(self, bulb_type):
        assert(type(bulb_type)==str)
        if bulb_type == "":
            self.bulb_type = self.bulb_types[0]

        elif bulb_type in self.bulb_types:
            self.bulb_type = bulb_type
            return True

        else:
            return False

    def get_bulb_type(self):
        return self.bulb_type
       

    def set_wattage(self, wattage=None):
        #set by given wattage
        if wattage:
            new_wattage = wattage

        #set by house size and number of occupants
        elif self.square_footage and self.occupants:
            if self.bulb_type == 'LED':
                #8 watts per bulb, usually 3 or more on a circuit
                new_wattage = 8 * (1 + self.square_footage/600 + self.occupants)
            elif self.bulb_type == 'halogen':
                #60-80 watts usually 1-3 on a circuit
                new_wattage = 40 * (1 + self.square_footage/600 + self.occupants)
            elif self.bulb_type == 'incandescent':
                #80-100 watts usually 1-3 on a circuit
                new_wattage = 50 * (1 + self.square_footage/600 + self.occupants)
        #set to default
        elif not wattage and not (self.square_footage and self.occupants):
            new_wattage = self.default_wattage

        if super().set_wattage(new_wattage): return True
        return False
        
    def prompt(self,get_input=input):
        bulb_type = get_input("enter light bulb type (default: " + self.bulb_types[0] + ") >")
                  
        #no entry, use default
        if not bulb_type:
            if self.set_bulb_type(self.bulb_types[0]):
                return True
            return False
        
        else:
            if self.set_bulb_type(bulb_type):
                return True
            else:
                print("Error: Input invalid!")
                print("should be one of ")
                for element in self.bulb_types:
                      print("   ",element, ",")
                self.prompt(get_input)
        