from eleclib.appliances.appliance import Appliance
from eleclib.utility import *

'''
##HEATER
###INTRO:
A HEATER varies greatly in output based on environmental conditions.
As such defining wattage of an electrical heater is only relevant for 
the purpose of calculating currrent draw, while power consumption is
related to the efficiency of the heater, the temperature outside and 
the building structure.

###USAGE:
You can either initialize a Heater without parameters and set the 
relevant values through the command prompt:
>myHeater = Heater()
>myHeater.prompt()

OR- You can pass values into the constructor directly. In this case
you should pass in EITHER **power_type, wattage, daily_usage** if these
values are known OR **power_type, wattage, efficiency**  AND **house** OR
**square_footage, R_walls, R_roof** where efficiency is a percentage, house 
is of type Household and R-values are full wall construction R values.
>myHouse = Household()
>myHeater = Heater(power_type = 'electric', wattage = 4000, efficiency = 90, house= myHouse)

Finally you can use its various reporting methods:
>print(str(myHeater))
>myFridge.get_consumption() #daily consumption average

###TODO: 
* support for seasonal changes- see get_consumption args
* perfect the get_consumption calculations
* add efficiency to prompt

'''

HEATER_TYPES = ["gas","wood","baseboard-electric","geo-electric","infloor-electric","none"]
#efficiency of heating type percentage- same order as HEATER_TYPES
HEATER_EFFICIENCIES = [None, None, 80, 200, 90, None]
DEFAULT_HEATER_WATTAGE = 5000
HEATER_WATTAGE_RANGE = [100,20000]

class Heater(Appliance):

    def __init__(self, power_type = HEATER_TYPES[0],
                 wattage=DEFAULT_HEATER_WATTAGE, 
                 square_footage = None,
                 daily_usage = None,
                 efficiency = None,
                 R_walls= None,
                 R_roof = None,
                 house = None):
        
        super().__init__(DEFAULT_HEATER_WATTAGE,
                         HEATER_WATTAGE_RANGE,
                         'heater',
                         types = HEATER_TYPES, 
                         power_type = power_type,
                         wattage = wattage,
                         daily_usage = daily_usage,
                         house = house)
            
        #self.set_efficiency(efficiency)
        if not house:
            self.square_footage = square_footage
            self.R_walls = R_walls
            self.R_roof = R_roof
        
    def set_from_house(self, house):
        '''
        get square_footage, and R_values from house
        later get location as well
        '''
        self.square_footage = house.get_square_footage()
        self.R_roof = house.get_R_roof()
        self.R_walls = house.get_R_walls()
        
        return True
        
    def get_usage(self):
        if self.usage:
            return self.usage
        else:
            return self.get_consumption()/24
        
    def set_type(self, power_type=None):
        '''
        set self.power_type and then if it works, set_efficiency()
        '''
        if super().set_type(power_type):
            if self.set_efficiency():
                return True
        return False
        
    def set_efficiency(self, e = None):
        if e:
            assert(type(e)==int)
            self.efficiency = e
            return True
        else:
            typeIdx = self.types.index(self.power_type)
            self.efficiency = HEATER_EFFICIENCIES[typeIdx]
            return True
        return False
    
    def get_efficiency(self):
        return self.efficiency
        
    def get_consumption(self, days=1,  peak=False):
        '''
        This method is rough!- fine estimate for now
        this will caculate the power consumption based on the type of heater, efficiency,
        square footage of space being heated and insulation values
        TODO: add in a parameter for location that will get local weather data for this
        
        heat loss per square meter = temp diff(celcius)/R-value
        for now avg_temp_diff = 10 (half the year,averaging 0 degrees)
        square_meters = square_footage/9
        assume 60/40 split in width vs length of house (shape_factor=.6)
        calculations are metric
        '''
    
        avg_temp_diff = 10
        footprint = self.square_footage/9
        storeys = 2
        height = storeys*3
        shape_factor = 0.6
        length = shape_factor*np.sqrt(footprint/(shape_factor*(1-shape_factor)))
        width = (1-shape_factor)*np.sqrt(footprint/(shape_factor*(1-shape_factor)))
        wall_area = 2*length*height+2*width*height
        loss_area = wall_area+footprint
        rise_factor = 0.6 #effect of more heat being lost to the top of a structure
        R_avg = (footprint * self.R_roof * rise_factor + wall_area * self.R_walls * (1-rise_factor))*2 / (footprint + wall_area)

        watts_loss = (footprint + wall_area)*avg_temp_diff/R_avg
        daily_loss = watts_loss*24#theoretical heat loss
        
        return loss*days*self.get_efficiency()
    