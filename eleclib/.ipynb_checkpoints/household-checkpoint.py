from eleclib.utility import extract_number, add_indent
from eleclib.appliances import *
from numbers import Number

'''
# Class Household
A Household contains information about the appliances in a house,
the number of occupants, the construction of the building, location,
and other info about the surroundings. 
It provides methods for sizing off-grid solutions, storing data to 
various file types, and calculating values like total power consumption,
maximum current draw, etc. which are useful in sizing electrical panels 
and cables.

### USAGE
You can initialize a Household without parameters and then define the 
parameters via command prompts
>myHouse = Household()\
>myHouse.prompt_for_args()

OR You can pass in arguments to the constructor:

Finally you can use the reporting methods to generate
files, and calculate relevant values.
>print(str(myHouse))\
>myHouse.get_consumption()\
>myHouse.get_max_current()

### TODO: 
* add support for propane-electric which may be run on propane part of 
the year and electric the rest.
* programmatic input- add argument unit
* reporting methods- reinstate
* add a has_been_set variable so we know to prompt about default or current value...
   
'''

DEFAULT_SQUARE_FOOTAGE = 6000
SQUARE_FOOTAGE_RANGE = [100,20000]

#R-VALUES BASED ON CURRENT BUILDING CODE VALUES FOR CANADA (Ontario 2021)
DEFAULT_R_ROOF = 30
DEFAULT_R_WALLS = 24
R_RANGE = [0,100]

DEFAULT_OCCUPANTS = 3
OCCUPANTS_RANGE = [1,100]

class Household(object):
    def __init__(self, 
        square_footage: int = None, 
        R_roof: float = None, 
        R_walls: float = None,
        off_grid = False,
        occupants: int = None, 
        appliances = [
                      "heater", 
                      "water heater", 
                      "fridge", 
                      "lights", 
                      "pump", 
                      "oven"
                     ],
        **kwargs):
        self.default_sf = 6000
        self.sf_range = [100, 20000]
        self.default_R_roof = 30
        self.default_R_walls = 24
        self.R_range = [1, 100]
        self.default_occupants = 3
        self.occupants_range = [1, 100]
        
        self.set_R_roof(R_roof)
        self.set_R_walls(R_walls)
        self.set_square_footage(square_footage)
        self.set_occupants(occupants)
        self.set_off_grid(off_grid)
        self.set_appliances(appliances)
    
    def load_from_file(self, file):
        return False
    
    def set_appliances(self, appliances):
        '''
        Pass appliances in as a list of strings containing appliance names,
        or as a list of objects for each appliance
        '''
        self.appliances = []
        appliance_names = {"heater": Heater,
                           "water heater": WaterHeater,
                           "fridge": Fridge,
                           "lights": Lights,
                           "pump": Pump,
                           "oven": Oven}
        
        for appliance in appliances:
            if type(appliance)==str:
                appliance = appliance.lower()
                if appliance in appliance_names:
                    self.appliances.append(
                        appliance_names[appliance](household = self))
                else:
                    raise Exception("supplied appliance name in ",
                                    "Household.set_appliances does not exist")
            elif issubclass(appliance,Appliance):
                self.appliances.append(appliance)
            else:
                raise TypeError("Error Household.set_appliances should",
                                "get a list of type str or Appliance")
        return True
    
        
    def __str__(self):
        text = "------------Household------------\n"
        text += "square footage: " + str(self.square_footage) + " square feet\n"
        text += "Appliances: \n"
        for appliance in self.appliances:
            text += add_indent(str(appliance), 4)
        text += "roof insulation: R-" + str(self.R_roof) + "\n"
        text += "wall insulation: R-" + str(self.R_walls) + "\n"
        return text
            
#--------------------------SETTER METHODS------------------------------------

    def set_square_footage(self,square_footage: int = None):
        if square_footage:
            assert self.square_footage_valid(square_footage)
            self.square_footage = square_footage
        else:
            self.square_footage = self.default_sf
            
    def set_R_roof(self,R_roof: float = None):
        if R_roof:
            assert self.R_valid(R_roof)
            self.R_roof = R_roof
        else:
            self.R_roof = self.default_R_roof
            
    def set_R_walls(self,R_walls: int = None):   
        if R_walls:
            assert self.R_valid(R_walls)
            self.R_walls = R_walls
        else:
            self.R_walls = self.default_R_walls
            
    def set_occupants(self,occupants: int = None):
        if occupants:
            assert self.occupants_valid(occupants)
            self.occupants = occupants
        else:
            self.occupants = self.default_occupants

    
    def set_off_grid(self, off):
        assert(type(off)==bool)
        self.off_grid = off
        
#------------------GETTERS------------------------------------------
    
    def get_square_footage(self):
        return self.square_footage
    
    def get_R_roof(self):
        return self.R_roof
    
    def get_R_walls(self):
        return self.R_walls
    
    def get_occupants(self):
        return self.occupants
    
#--------------checks-----------------------------------------------

    def square_footage_valid(self, sf: int):
        if type(sf) == int and self.sf_range[0]<=sf<=self.sf_range[1]:
            return True
        else:
            return False
        
    def R_valid(self, R_val: float):
        if (isinstance(R_val, Number)
                and self.R_range[0]<=R_val<=self.R_range[1]):
            return True
        else:
            return False
        
    def occupants_valid(self, occupants: int):
        if (type(occupants) == int 
                and self.occupants_range[0] <= occupants <= self.occupants_range[1]):
            return True
        else:
            return False
        
    
#------------------PROMPTING FOR SETUP-------------------------------------

    def get_input(self, message):
        '''
        This method is for testing purposes (and good code structure). 
        It allows the prompt_* methods to be decoupled from the stdin so that 
        we can inject test case values in place of manual testing.
        '''
        return input(message)
    
    def prompt_for_args(self):
        print("Creating new household...")
        print("Enter values specified or ENTER to use defaults")
        
        self._prompt_sf()
        self._prompt_R_roof()
        self._prompt_R_walls()
        self._prompt_occupants()
        
        for appliance in self.appliances:
            appliance.prompt(get_input=self.get_input)       
        
        #self.water_heater.set_usage(occupants=self.occupants)
        
    def _prompt_sf(self):
        square_footage_raw = self.get_input("enter square footage (default: " 
                                            + str(self.default_sf) 
                                            + ") >")
        
        if not square_footage_raw:
            self.set_square_footage(self.default_sf)
        
        else:
            square_footage = int(extract_number(square_footage_raw))
            if self.square_footage_valid(square_footage):
                self.set_square_footage(square_footage)
                
            else:
                print("Error: Input invalid!")
                min_val = SQUARE_FOOTAGE_RANGE[0]
                max_val = SQUARE_FOOTAGE_RANGE[1]
                print("should be an integer between ", min_val, 
                      " and ", max_val, 
                      " representing the total square footage of the house")
                self._prompt_sf()
                           
                    
    def _prompt_R_roof(self):
        R_roof = self.get_input("enter roof insulation R-value (default: " 
                                + str(self.default_R_roof) 
                                + ") >")
        #no entry, use default
        if not R_roof:
            self.set_R_roof(self.default_R_roof)
                      
        else:
            R_roof = extract_number(R_roof)
            if self.R_valid(R_roof):
                self.set_R_roof(R_roof)
            else:
                print("Error: Input invalid!")
                min_val = self.R_range[0]
                max_val = self.R_range[1]
                print("should be an integer between ", 
                      min_val, 
                      " and ", 
                      max_val, 
                      " representing the R-value of insulation in the roof")
                self._prompt_R_roof()

        
    def _prompt_R_walls(self):
        R_walls = self.get_input("enter wall insulation R-value (default: " 
                                 + str(self.default_R_walls) 
                                 + ") >")
        #no entry, use default
        if not R_walls:
            self.set_R_walls(self.default_R_walls)
            
        else:
            R_walls = extract_number(R_walls)
            if self.R_valid(R_walls):
                self.set_R_walls(R_walls)
            else:
                print("Error: Input invalid!")
                min_val = self.R_range[0]
                max_val = self.R_range[1]
                print("should be an integer between ", 
                      min_val, 
                      " and ", 
                      max_val, 
                      " representing the R-value of insulation in",
                      "the exterior walls")
                self._prompt_R_walls()
         
    
    def _prompt_occupants(self):
        occupants = self.get_input("enter number of occupants (default: " 
                                   + str(self.default_occupants) 
                                   + ") >")
        #no entry, use default
        if not occupants:
            self.set_occupants(self.default_occupants)
                      
        else:
            occupants = int(extract_number(occupants))
            if self.occupants_valid(occupants):
                self.set_occupants(occupants)
            else:
                print("Error: Input invalid!")
                min_val = self.occupants_range[0]
                max_val = self.occupants_range[1]
                print("should be an integer between ", 
                      min_val, 
                      " and ", 
                      max_val, 
                      " representing the number of occupants")
                self._prompt_occupants()
         
        
#--------------------------------REPORTING AND RECOMMENDATIONS----------------

    def get_consumption(self, days: int = 1, peak: bool = False):
        
        total = 0
        for appliance in self.appliances:
            total += appliance.get_consumption()
        
        return total/1000
    
    def get_peak_current(self):
        
        total = 0
        for appliance in self.appliances:
            total += appliance.get_peak_current()
        #total value is scaled back since all appliances will never be 
        #running all at the same time
        scaling_factor = 0.75
        return total*scaling_factor
        
        

   
    def get_recommendations(self):
        recommendations = []
        
        if self.light_bulbs != LED:
            recommendations.append(
                "You should switch to LED lighting!",
                "It uses much less power than older varieties")
            
        if self.off_grid:
            if self.fridge.power_type == "electric":
                recommendations.append(
                    "Switch to a low voltage fridge. They are much more",
                    "efficient than the alternatives. Being off-grid you",
                    "already have low voltage power on site!")
                
        if self.R_roof < 30 or R_walls < 24:
            recommendations.append(
                "Your insulation is less than modern building code",
                "(for Ontario). It could be worth upgrading next time",
                "you have access to it.")
            
        if self.square_footage > (1000 + self.occupants*400):
            recommendations.append(
                "You probably don't need so much space. Consider down-sizing")
        
        return recommendations
    
    
    
'''
    def report(format="xlsx"):
        
        #Format data with columns [appliance, yearly power(kwh), max current(A)]
        
        index = []
        data_rows = []
        if self.oven_is_electric():
            index.append("oven")
            data_rows.append([self.get_oven_usage*365/1000, self.oven_wattage/240])
        if self.water_heater_is_electric():
            data_rows.append([self.water_heater_wattage*WATER_HEATER_USAGE_DAILY*365, self.water_heater_wattage/self.water_heater_voltage])
        
        index.append("")
        #create dataframe
        df = pd.DataFrame([[]])
           
        return False
    '''