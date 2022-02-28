import pandas as pd
from numbers import Number
from eleclib.utility import extract_number

'''
##APPLIANCE
###INTRO:
An appliance is defined by name, power type, wattage and usage.
These values in turn let us calculate its contribution to total
current draw and power consumption for a Household.

###USAGE:
Private class used only by its children.

###TODO: 
* appliances are not all interchangeable, different appliances
rely on different values to get wattage and daily_usage...
* create a AustomAppliance class that can be used to create an
appliance that has not been added already. This should not need
certain values like types and default values.
* when prompting "" should leave the current value rather than set the 
default?
* add support for propane/gas type appliances to calculate volumetric
usage

'''
DEFAULT_APPLIANCE_TYPES = ['electric','gas','none']

  
class Appliance(object):
    
    def __init__(self,
                default_wattage, 
                wattage_range,
                name, 
                types=DEFAULT_APPLIANCE_TYPES, 
                power_type = None,
                wattage = None,
                daily_usage = None,
                b_prompt_usage = False,
                house = None):
        self.b_prompt_usage = b_prompt_usage
        #required arguments
        if not type(wattage_range)==list and not len(wattage_range)==2:
            raise ValueError("Error: invalid wattage_range supplied to Appliance")
        
        if not wattage_range[0] <= default_wattage <= wattage_range[1]:
            raise ValueError("Error: invalid default_wattage supplied to Appliance")

        self.set_wattage_range(wattage_range)
        self.set_default_wattage(default_wattage)
        self.name = name
        
        #optional arguments
        self.set_types(types)
        self.default_type = self.types[0]
        self.set_type(power_type)
        
        #if Household object is supplied get any info we need from it
        #this could affect set_usage, execute before next call
        if house:
            self.set_from_house(house)
            
        self.set_usage(daily_usage)
        self.set_wattage(wattage)
        
        
        
        
    def __str__(self):
        text = self.name + " type: " + self.power_type + "\n"
        if self.is_electric():
            text += self.name + " wattage: " + str(self.get_wattage()) + " watts\n"
        return text

    
    #-------------SETTERS------------------------
    
    def set_from_house(self, house):
        '''
        If appliance relies on values from household configuration populate them here.
        This can be called from Household if anything is updated at that level
        '''
        return True
    
    def set_types(self, types):
        assert(type(types)==list)
        assert(len(types)>0)
        assert(type(types[0]==str))
        self.types = types
    
    
    def set_type(self, power_type=None):
        #empty string or None- set default
        if not power_type:
            self.power_type = self.types[0]
            return True
        #valid type supplied
        elif power_type in self.types:
            self.power_type = power_type
            return True
        else:
            return False
    
    def set_default_wattage(self, wattage = None):
        assert(isinstance(wattage,Number))
        self.default_wattage = wattage
    
                
    def set_wattage_range(self, wattage_range):
        assert(type(wattage_range)==list)
        assert(len(wattage_range)==2)
        self.wattage_range = wattage_range
    
    def set_wattage(self, wattage = None):
        if wattage and isinstance(wattage,Number):
            if self.wattage_range[0] <= wattage <= self.wattage_range[1]:
                self.wattage = wattage
                return True
        elif not wattage:
            self.wattage = self.default_wattage
        return False
        
    def set_usage(self, daily_usage):
        if daily_usage:
            assert(isinstance(daily_usage,Number))
            if 0 <= daily_usage <= 24:
                self.usage = daily_usage
                return True
            else:
                raise ValueError("Error: daily_usage out of bounds, should be between 0 and 24")
        else:
            self.usage = 0
            return True
    
    #-----------GETTERS------------------------------       
    def is_electric(self):
        if "electric" in self.power_type:
            return True
        return False
    
    def get_wattage(self):
        return self.wattage
    
    def get_usage(self):
        return self.usage
    
    def get_consumption(self, days=1, peak=False):
        '''
        get the power consumption over given number of days
        if peak is True get the worst case (ie. winter for heaters)
        this should be overriden for most cases
        '''
        wattage = self.get_wattage()
        usage = self.get_usage()
        if wattage and usage and days:
            assert(isinstance(wattage,Number))
            assert(isinstance(usage,Number))
            assert(isinstance(days,Number))
            consumption = wattage*usage*days
            return consumption
        return False
    
    #---------PROMPTS---------------------------------
    
    def prompt(self, get_input=input):
        #define a user prompt given input_channel(function) as the input mechanism
        self.prompt_type(get_input)
        if self.is_electric():
            self.prompt_wattage(get_input)
        if self.b_prompt_usage:
            self.prompt_usage(get_input)
            
    def prompt_type(self, get_input):
        appliance_type = get_input("enter " + self.name + " power type (default: " + self.default_type + ") >")
                  
        #no entry, use default
        if not appliance_type:
            if self.set_type(self.default_type):
                return True
            return False
        
        else:
            if self.set_type(appliance_type):
                return True
            else:
                print("Error: Input invalid!")
                print("should be one of ")
                for element in self.types:
                      print("   ",element, ",")
                self.prompt_type(get_input)
        return False
        
    
    def prompt_wattage(self, get_input):
        wattage_raw = get_input("enter " + self.name + " wattage (default: " + str(self.default_wattage) + ") >")
        #no entry, use default
        if not wattage_raw:
            assert(self.is_electric())
            if self.set_wattage(self.default_wattage):
                return True
            return False
                      
        else:
            wattage = extract_number(wattage_raw)
            if wattage and self.set_wattage(wattage):
                return True
            else:
                print("Error: Input invalid!")
                min_val = self.wattage_range[0]
                max_val = self.wattage_range[1]
                print("should be an integer between ", min_val, " and ", max_val, " representing the rated power in watts")
                self.prompt_wattage(get_input)
                
    def prompt_usage(self, get_input):
        usage_raw = get_input("enter " + self.name + " usage (in hours)>")
        #no entry, use default
        if not usage_raw:
            if self.set_usage(0):
                return True
            return False
                      
        else:
            usage = extract_number(usage_raw)
            if usage and self.set_usage(usage):
                return True
            else:
                print("Error: Input invalid!")
                self.prompt_usage(get_input)
                
    #----------------FILE-STORAGE-----------------
    #TODO: to_dataframe()
    #      from_dataframe()
    #      from_text()
    
 