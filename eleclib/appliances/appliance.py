from numbers import Number
from eleclib.utility import extract_number, list_type
from typing import List
from abc import ABCMeta, abstractmethod


class Appliance(metaclass=ABCMeta):
    '''
    =================
    Class Appliance
    =================
    
    This is a Private class used to create a template for various specific 
    appliances.
    
    '''
    def __init__(self,
                name: str,
                power_types: List[str],
                wattage_range: List[int],
                default_wattage: Number,
                power_type: str = None
                ):
        
        self._set_name(name)
        self._set_power_types(power_types)
        self._set_wattage_range(wattage_range)
        self._set_wattage_default(default_wattage) 
        self.default_type = self.power_types[0]
        self._set_power_type(power_type)
        
    def __str__(self):
        return (self.name.capitalize() 
                + " (" + self.power_type + "):")
    
    def _set_name(self, name: str):
        assert type(name)==str
        self.name = name

    def _set_power_types(self, power_types: List[str]):
        assert list_type(power_types, str)
        assert len(power_types) >= 1
        self.power_types = power_types
        
    def _set_wattage_range(self, wattage_range: List[int]):
        assert list_type(wattage_range, int)
        assert len(wattage_range)==2
        assert wattage_range[1] >= wattage_range[0]
        self.wattage_range = wattage_range
        
    def _set_wattage_default(self, wattage: Number):
        assert isinstance(wattage, Number)
        self.default_wattage = wattage
      
    def _set_power_type(self, power_type: str = None):
        if power_type:
            assert type(power_type) == str
            assert self._valid_type(power_type)
            self.power_type = power_type
        else:
            self.power_type = self.default_type

    def _valid_type(self, power_type):
        if type(power_type) == str and power_type in self.power_types:
            return True
        else:
            return False
        
    def _wattage_in_range(self, wattage: float):
        if (isinstance(wattage, Number) 
                and self.wattage_range[0] <= wattage <= self.wattage_range[1]):
            return True
        else:
            return False
        
    def is_electric(self):
        if "electric" in self.power_type:
            return True
        return False
    
    
    @abstractmethod
    def get_consumption(self, days: int = 1, peak: bool = False):
        '''
        get consumption in watt-hours for the given period days
        if peak- get maximum value for given period
        (ie. worst day of the year if day is set to 1)
        '''
        pass
    
    @abstractmethod
    def get_peak_current(self, voltage: int = 120, standalone: bool = False):
        '''
        get peak current
        useful for sizing electrical panels, main power lines, solar 
        components, etc.
        if standalone, get the actual peak value else get the value to be used for getting
        the total household amount. This is often scaled back for appliances that 
        do not remain at peak value for long...
        '''
        pass
    
    @abstractmethod
    def prompt(self, get_input = input):
        '''
        method: prompt()
        set up the relevant parameters for each given appliance through interactive 
        command-line prompts
        '''
        pass
        
    def _prompt_type(self, get_input = input):
        appliance_type = get_input("enter " 
                                   + self.name 
                                   + " power type (default: " 
                                   + self.default_type 
                                   + ") >")
                  
        #no entry, use default
        if not appliance_type:
            self._set_power_type(self.default_type)
        
        else:
            if self._valid_type(appliance_type):
                self._set_power_type(appliance_type)
            else:
                print("Error: Input invalid!")
                print("should be one of ")
                for element in self.power_types:
                      print("   ",element, ",")
                self._prompt_type(get_input)
                
    def _prompt_wattage(self, get_input):
        wattage_raw = get_input("enter " 
                                + self.name 
                                + " wattage (default: " 
                                + str(self.default_wattage) 
                                + ") >")
        #no entry, use default
        if not wattage_raw:
            self._set_wattage(self.default_wattage)
                      
        else:
            wattage = int(extract_number(wattage_raw))
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