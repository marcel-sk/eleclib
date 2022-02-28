from eleclib.appliances.appliance import Appliance
from eleclib.utility import add_indent
from numbers import Number
from abc import ABCMeta, abstractmethod
from typing import List
import math
'''
=======================
Household-Based Appliance
=======================

Defines appliances whose load is determined only by household parameters like
location, occupants, etc.
'''

class HouseholdAppliance(Appliance, metaclass=ABCMeta):
    '''
    ======================
    class HouseholdAppliance
    ======================
    
    '''
    
    def __init__(self,
                name: str,
                power_types: List[str],
                wattage_range: List[int],
                default_wattage: Number,
                uses_occupants: bool = False,
                uses_R_values: bool = False,
                uses_square_footage: bool = False,
                power_type: str = None,
                household = None,
                occupants: int = None,
                R_walls: int = None,
                R_roof: int = None,
                square_footage: int = None):
        
        super().__init__(name,
                         power_types,
                         wattage_range,
                         default_wattage,
                         power_type = power_type)
        
        #--------------------------------------
        #select the household values we are using
        self.uses_occupants = uses_occupants
        self.uses_R_values = uses_R_values
        self.uses_square_footage = uses_square_footage
        
        self._set_household(household)
        
        if self.uses_occupants:
            self.default_occupants = 3
            self._set_occupants(occupants)
            
        if self.uses_R_values:
            self.R_walls_default = 24
            self.R_roof_default = 30
            self._set_R_walls(R_walls)
            self._set_R_roof(R_roof)
        
        if self.uses_square_footage:
            self.square_footage_default = 6000
            self._set_square_footage(square_footage)
            
    def __str__(self):
        return super().__str__()
  
        
    def _set_household(self, household = None):
        if household:
            self.household = household
            self.update()
           
        else:
            self.household = None
    
    def _set_occupants(self, occupants: int = None):
        #self.household overrides inputs
        if self.household:
            self.occupants = self.household.get_occupants()
                 
        elif occupants:
            assert type(occupants) == int
            self.occupants = occupants
                 
        else:
            self.occupants = self.default_occupants
            
    def _set_square_footage(self, square_footage: int = None):
        if self.household:
            self.square_footage = self.household.get_square_footage()
        elif square_footage:
            assert type(square_footage)==int
            self.square_footage = square_footage
        else:
            self.square_footage = self.square_footage_default
                 
    def _set_R_roof(self, R_roof: int = None):
        
        if self.household:
            self.R_roof = self.household.get_R_roof()
        elif R_roof:
            assert type(R_roof)==int
            self.R_roof = R_roof
        else:
            self.R_roof = self.R_roof_default
            
                 
    def _set_R_walls(self, R_walls: int = None):
        
        if self.household:
            self.R_walls = self.household.get_R_walls()
            
        elif R_walls:
            assert type(R_walls)==int
            self.R_walls = R_walls
            
        else:
            self.R_walls = self.R_walls_default
        
    def update(self):
        #update local values from self.household
        if self.uses_occupants:
            self._set_occupants()
            
        if self.uses_R_values:
            self._set_R_walls()
            self._set_R_roof()
        
        if self.uses_square_footage:
            self._set_square_footage()
                 
    
    def prompt(self, get_input = input):
        self._prompt_type(get_input)
        if self.is_electric():
            self._prompt_wattage(get_input)
        if not self.household:
            self._prompt_household(get_input)
       
    
    def _prompt_household(self, get_input = input):
        if self.uses_occupants:
            self._prompt_occupants(get_input)
            
        if self.uses_R_values:
            self._prompt_R_values(get_input)
        
        if self.uses_square_footage:
            self._prompt_square_footage()

        
    def _prompt_occupants(self, get_input = input):
        occupants_raw = get_input("enter number of occupants in household>")
        #no entry, use default
        if not occupants_raw:
            self._set_occupants(self.default_occupants)
                      
        else:
            occupants = int(extract_number(occupants_raw))
            if occupants:
                self._set_occupants(occupants)
            else:
                print("Error: Input invalid!")
                print("should be an integer between 1 and 20")
                self._prompt_household(get_input)
                 
    def _prompt_square_footage(self, get_input = input):
        sf_raw = get_input("enter square footage of household>")
        #no entry, use default
        if not sf_raw:
            self._set_square_footage(self.square_footage_default)

        else:
            sf = int(extract_number(sf_raw))
            if sf:
                self._set_square_footage(sf)
            else:
                print("Error: Input invalid!")
                self._prompt_square_footage(get_input)
                
    def _prompt_R_vals(self, get_input = input):
        self._prompt_R_walls(get_input)
        self._prompt_R_roof(get_input)
        
        
    def _prompt_R_walls(self, get_input = input):
        R_raw = get_input("enter wall insulation of household (R value)>")
        #no entry, use default
        if not R_raw:
            self._set_R_walls(self.R_walls_default)

        else:
            R_val = extract_number(R_raw)
            if R_val:
                self._set_R_walls(R_val)
            else:
                print("Error: Input invalid!")
                self._prompt_R_walls(get_input)
                
    def _prompt_R_roof(self, get_input = input):
        R_raw = get_input("enter roof/attic insulation of household (R value)>")
        #no entry, use default
        if not R_raw:
            self._set_R_roof(self.R_roof_default)

        else:
            R_roof = extract_number(R_raw)
            if R_roof:
                self._set_R_roof(R_roof)
            else:
                print("Error: Input invalid!")
                self._prompt_R_roof(get_input)
                
                
    @abstractmethod
    def get_consumption(self, days: int = 1, peak: bool = False):
        #get power consumption to be implemented by each subclass
        pass
    
    @abstractmethod
    def get_peak_current(self, voltage: int = 120, standalone: bool = False):
        #get peak current to be implemented by each subclass
        pass
    
class Pump(HouseholdAppliance):
    '''
    ======================
    class Pump
    ======================
    
    '''
    
    def __init__(self,
                 power_type: str = None,
                 wattage: int = None,
                 occupants: int = None,
                 household = None):
                 
                 
        super().__init__('pump',
                         ['electric', 'electric-low-volt', 'propane'],
                         [50, 15000],
                         2000,
                         uses_occupants = True,
                         power_type = power_type,
                         household = household,
                         occupants = occupants)
 
        self._set_wattage(wattage)
    
    def __str__(self):
        title = super().__str__() + '\n'
        indent = "wattage: " + str(self.wattage) + "\n"
        indent += ("yearly consumption: " 
                + str(self.get_consumption(days=365)/1000)
                + " Kwh\n")
        indent = add_indent(indent,4)
        str_rep = title + indent
        return str_rep
    
    def _set_wattage(self, wattage: int = None):
        if wattage:
            assert type(wattage)==int
            assert self._wattage_in_range(wattage)
            self.wattage = wattage
        else:
            self.wattage = self.default_wattage
                 
    def get_peak_current(self, voltage: int = 120, standalone: bool = False):
        self.update()
        if standalone:
            peak_wattage = self.wattage
        else:
            peak_factor = 1.5
            peak_wattage = self.wattage*peak_factor
        return peak_wattage/voltage
        
    def get_consumption(self, days: int = 1, peak: bool = False):
        usage = 1 + 0.5*(self.occupants-1)
        return usage*self.wattage*days
        
                 
class WaterHeater(HouseholdAppliance):
    '''
    ======================
    class WaterHeater
    ======================
    
    '''
    
    def __init__(self,
                 power_type: str = None,
                 wattage: int = None,
                 occupants: int = None,
                 household = None):
                 
        super().__init__('water heater',
                         ['electric', 'propane'],
                         [500, 15000],
                         4000,
                         uses_occupants = True,
                         power_type = power_type,
                         household = household,
                         occupants = occupants)
                 
        self._set_wattage(wattage)
        
    def __str__(self):
        title = super().__str__() + '\n'
        indent = "wattage: " + str(self.wattage) + "\n"
        indent += ("yearly consumption: " 
                + str(self.get_consumption(days=365)/1000)
                + " Kwh\n")
        indent = add_indent(indent,4)
        str_rep = title + indent
        return str_rep
                 
    def _set_wattage(self, wattage: int = None):
        if wattage:
            assert type(wattage)==int
            assert self._wattage_in_range(wattage)
            self.wattage = wattage
        else:
            self.wattage = self.default_wattage
 
    def get_peak_current(self, voltage: int = 120, standalone: bool = False):
        assert type(voltage)==int
        return self.wattage/voltage
    
    def get_consumption(self, days: int = 1, peak: bool = False):
        self.update()
        usage = 2 + self.occupants
        daily_wattage = usage*self.wattage
        return daily_wattage*days   
                 
class Heater(HouseholdAppliance):
    '''
    ======================
    class Heater
    ======================
    
    '''
    
    def __init__(self,
                 power_type: str = None,
                 wattage: int = None,
                 square_footage: int = None,
                 R_roof: int = None,
                 R_walls: int = None,
                 household = None):
                 
        super().__init__('heater',
                         ['electric', 'gas', 'propane', 'wood', 'geothermal'],
                         [500, 20000],
                         4000,
                         uses_square_footage = True,
                         uses_R_values = True,
                         power_type = power_type,
                         household = household,
                         square_footage = square_footage,
                         R_roof = R_roof,
                         R_walls = R_walls)
        
        self._set_wattage(wattage)
        
    def __str__(self):
        title = super().__str__() + '\n'
        indent = "wattage: " + str(self.wattage) + "\n"
        indent += ("yearly consumption: " 
                + str(self.get_consumption(days=365)/1000)
                + " Kwh\n")
        indent = add_indent(indent,4)
        str_rep = title + indent
        return str_rep
        
    def _set_wattage(self, wattage: int = None):
        if wattage:
            assert isinstance(wattage, Number)
            assert self._wattage_in_range(wattage)
            self.wattage = wattage
        else:
            self.wattage = self.default_wattage
            
    def get_consumption(self, days: int = 1, peak: bool = False):
        '''
        This method is rough!- fine estimate for now
        this will caculate the power consumption based on the type of heater, 
        efficiency, square footage of space being heated and insulation values
        TODO: add in a parameter for location that will get local weather 
        data for this
        
        heat loss per square meter = temp diff(celcius)/R-value
        for now avg_temp_diff = 10 (half the year,averaging 0 degrees)
        square_meters = square_footage/9
        assume 60/40 split in width vs length of house (shape_factor=.6)
        calculations are metric
        '''
        self.update()
        avg_temp_diff = 10
        footprint = self.square_footage/9
        storeys = 2
        height = storeys*3
        shape_factor = 0.6
        length = shape_factor*math.sqrt(footprint/(shape_factor*(1-shape_factor)))
        width = (1-shape_factor)*math.sqrt(footprint/(shape_factor*(1-shape_factor)))
        wall_area = 2*length*height+2*width*height
        loss_area = wall_area+footprint
        rise_factor = 0.6 #effect of more heat being lost to the top of a structure
        R_avg = (footprint * self.R_roof * rise_factor 
                + wall_area * self.R_walls * (1-rise_factor))*2/loss_area

        watts_loss = (footprint + wall_area)*avg_temp_diff/R_avg
        daily_loss = watts_loss*24#theoretical heat loss
        efficiency = 0.9
        
        return daily_loss*days*efficiency
    
    def get_peak_current(self, voltage: int = 120, standalone: bool = False):
        assert type(voltage)==int
        self.update()
        peak_current = self.wattage/voltage
                 
class Lights(HouseholdAppliance):
    '''
    ======================
    class Lights
    ======================
    
    '''
    
    def __init__(self,
                 bulb_type: str = None,
                 occupants: int = None,
                 square_footage: int = None,
                 household = None):
                 
        super().__init__('lights',
                         ['electric'],
                         [500, 15000],
                         4000,
                         uses_occupants = True,
                         uses_square_footage = True,
                         power_type = 'electric',
                         household = household,
                         occupants = occupants,
                         square_footage = square_footage)
        
        self.bulb_types = ['LED', 'incandescent', 'halogen']
        self.default_bulb = self.bulb_types[0]
        self._set_bulb_type(bulb_type)
        
    def __str__(self):
        title = self.name.capitalize() + ": \n"
        indent = "bulb type: " + str(self.bulb_type) + "\n"
        indent += ("yearly consumption: " 
                + str(self.get_consumption(days=365)/1000)
                + " Kwh\n")
        indent = add_indent(indent,4)
        return title + indent
                
    def _set_bulb_type(self, bulb_type: str = None):
        if bulb_type:
            assert type(bulb_type)==str
            assert self._valid_bulb(bulb_type)
            self.bulb_type = bulb_type
        else:
            self.bulb_type = self.default_bulb
            
    def _valid_bulb(self, bulb_type: str):
        if type(bulb_type) == str and bulb_type in self.bulb_types:
            return True
        else:
            return False
        
    
    def get_consumption(self, days: int = 1, peak: bool = False):
        avg_wattage = self.get_avg_wattage()
        consumption = avg_wattage * 24
        return consumption
    
    def get_peak_current(self, voltage: int = 120, standalone: bool = False):
        assert type(voltage)==int
        peak_wattage = self.get_avg_wattage() * 4
        peak_current = peak_wattage/voltage
        return peak_current
            
            
    def get_avg_wattage(self):
        self.update()
        if self.square_footage and self.occupants:
            if self.bulb_type == 'LED':
                #8 watts per bulb, usually 3 or more on a circuit
                avg_wattage = 8 * (1 + self.square_footage/600 + self.occupants)
            elif self.bulb_type == 'halogen':
                #60-80 watts usually 1-3 on a circuit
                avg_wattage = 40 * (1 + self.square_footage/600 + self.occupants)
            elif self.bulb_type == 'incandescent':
                #80-100 watts usually 1-3 on a circuit
                avg_wattage = 50 * (1 + self.square_footage/600 + self.occupants)
            else:
                raise Exception("Error: bulb type invalid when get_consumption called")
        else:
            avg_wattage = 0
        
        return avg_wattage
    
    def prompt(self, get_input = input):
        self._prompt_type(get_input)
        if not self.household:
            self._prompt_household(get_input)
    
    def _prompt_type(self, get_input = input):
        bulb_type = get_input("enter light bulb type (default: " 
                                   + self.default_bulb 
                                   + ") >")
                  
        #no entry, use default
        if not bulb_type:
            self._set_bulb_type(self.default_bulb)
        
        else:
            if self._valid_bulb(bulb_type):
                self._set_bulb_type(bulb_type)
            else:
                print("Error: Input invalid!")
                print("should be one of ")
                for element in self.bulb_types:
                      print("   ",element, ",")
                self._prompt_type(get_input)
                