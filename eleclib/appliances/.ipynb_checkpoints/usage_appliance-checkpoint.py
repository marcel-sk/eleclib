from eleclib.appliances.appliance import Appliance
from numbers import Number
from eleclib.utility import extract_number, extract_unit, \
                            convert_to_watts, UNITS, add_indent
from typing import List
'''
=======================
Usage-Based Appliance
=======================

Defines appliances whose usage time is known and whose load is dependant
entirely on wattage and usage
'''

class UsageAppliance(Appliance):
    '''
    =====================
    class UsageAppliance
    =====================
    
    '''
    
    def __init__(self,
                name: str,
                power_types: List[str],
                wattage_range: List[int],
                default_wattage: Number,
                default_usage: Number,
                wattage: int = None,
                usage: float = None,
                power_type: str = None,
                *args,
                **kwargs
                ):
        
        super().__init__(name,
                         power_types,
                         wattage_range,
                         default_wattage,
                         power_type = power_type)
        
        self._set_wattage(wattage)
        self._set_default_usage(default_usage)
        self._set_usage(usage)
        
    def __str__(self):
        title = super().__str__() + '\n'
        indent = ""
        if self.is_electric():
            indent += "wattage: " + str(int(self.wattage)) + "\n"
        indent += "usage: " + str(self.usage) + "\n"
        if self.is_electric():
            indent += ("yearly consumption: " 
                + str(self.get_consumption(days=365)/1000)
                + " Kwh\n")
        indent = add_indent(indent,4)
        str_rep = title + indent
        return str_rep
        
        
    def _set_wattage(self, wattage: float = None):
        if wattage:
            assert isinstance(wattage,Number)
            assert self._wattage_in_range(wattage)
            self.wattage = wattage
        else:
            self.wattage = self.default_wattage
            
    def _set_default_usage(self, usage: Number):
        assert isinstance(usage, Number)
        self.default_usage = usage
        
    def _set_usage(self, usage: float= None):
        if usage:
            assert isinstance(usage, Number)
            assert 0 <= usage <= 24
            self.usage = usage
        else:
            self.usage = self.default_usage
        
    def prompt(self, get_input = input):
        if len(self.power_types) > 1:
            self._prompt_type(get_input)
        if self.is_electric():
            self._prompt_wattage(get_input)
            
                
    def _prompt_usage(self, get_input):
        usage_raw = get_input("enter " 
                              + self.name 
                              + " usage (in hours)>")
        #no entry, use default
        if not usage_raw:
            self._set_usage(self.default_usage)
                
        else:
            usage = extract_number(usage_raw)
            if usage and self._usage_valid(usage):
                self._set_usage(usage)
            else:
                print("Error: Input invalid!")
                self._prompt_usage(get_input)
                
    def _usage_valid(self, usage: Number = None):
        if isinstance(usage, Number) and 0 <= usage <= 24:
            return True
        else:
            return False
    
    def get_peak_current(self, voltage: int = 120, standalone: bool = False):
        assert type(voltage) == int
        return self.wattage/voltage

    def get_consumption(self, days: int = 1, peak: bool = False):
        assert isinstance(days, Number)
        return self.wattage*self.usage*days
            
class Oven(UsageAppliance):
    '''
    ===========
    class Oven
    ===========

    '''
    
    def __init__(self,
                power_type: str = None,
                wattage: int = None,
                usage: float = None,
                **kwargs):
        
        super().__init__('oven',
                        ['gas', 'electric', 'electric-toaster'],
                        [1000,15000],
                        5000,
                        1,
                        wattage = wattage,
                        usage = usage,
                        power_type = power_type)
        
    def __str__(self):
        #this method has to be passed up the chain otherwise it will use
        #the built-in object class method 
        return super().__str__()
        
    def prompt(self, get_input):
        super().prompt(get_input)
        self._prompt_usage(get_input)
        
        
class Fridge(UsageAppliance):
    
    '''
    =============
    class Fridge
    =============

    '''
    def __init__(self,
                 power_type: str = None,
                 wattage: int = None,
                 unit: str = None,
                 usage: float = None,
                 **kwargs):
        
        if unit and not unit in UNITS['watts']:
            wattage = convert_to_watts(wattage, unit, usage)

        super().__init__('fridge',
                         ['electric', 'electric-low-volt', 'propane'],
                         [50,2000],
                         500,
                         8,
                         wattage = wattage,
                         usage = usage,
                         power_type = power_type)
        
    def __str__(self):
        #this method has to be passed up the chain otherwise it will use
        #the built-in object class method 
        return super().__str__()
    
    def _prompt_wattage(self, get_input):
        units = []
        for key in UNITS:
            units.append(key)
        print("enter " 
              + self.name 
              + " wattage, followed by a unit " 
              + str(units))
        wattage_raw = get_input ("default: " 
                                + str(self.default_wattage) 
                                + "watts >")
        #no entry, use default
        if not wattage_raw:
            self._set_wattage(self.default_wattage)
                      
        else:
            wattage = int(extract_number(wattage_raw))
            unit = extract_unit(wattage_raw)
            print('fridge wattage unit: ',unit)
            
            if unit == 'watts' and self._wattage_in_range(wattage):
                self._prompt_usage(get_input)

            wattage = int(convert_to_watts(wattage, unit, self.usage))
            if self._wattage_in_range(wattage):
                self._set_wattage(wattage)
                
            else:
                print("Error: Input invalid!")
                min_val = self.wattage_range[0]
                max_val = self.wattage_range[1]
                print("should be an integer between ",
                      min_val, " and ",
                      max_val, " representing the rated power in watts")
                self._prompt_wattage(get_input)

        