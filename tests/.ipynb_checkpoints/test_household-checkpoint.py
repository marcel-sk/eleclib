#from unittest.mock import create_autospec
import unittest
from unittest.mock import patch
from eleclib import __version__
from eleclib.household import *

class cmdInputTest(unittest.TestCase):
    
    def setUp(self):
        self.house = Household()                    
        
    '''
    ----------------------Test prompt_for_args()------------------
    '''

    '''
    test prompt_for_args() with a list of user input values. erroneous values followed by realistic inputs.
    '''
    @patch('eleclib.household.Household.get_input',side_effect=[
        "0",          #square footage- incorrect
        "100000",     #square footage- incorrect
        "1000sf",     #square footage- extra characters (acceptable)
        
        "1000",       #R roof- incorrect
        "34",         #R roof- correct
        "1000",       #R walls- incorrect
        "18",         #R walls- correct
        
        "text",       #occupants- incorrect
        "1000",       #occupants- incorrect
        "4",          #occupants- correct
        
        "gap",        #heating type- incorrect
        "gas",        #heating type- correct
        
        "electrik",   #water heater type- incorrect
        "electric",   #water heater type- correct
        "10",         #water heater wattage- incorrect
        "100000",     #water heater wattage- incorrect
        "2500 watts", #water heater wattage- acceptable
        
        "electrik",   #fridge type- incorrect
        "electric",   #fridge type- correct
        "10",         #fridge wattage- incorrect
        "100000",     #fridge wattage- incorrect
        "250 watts",  #fridge wattage- correct
        "100",        #fridge usage- incorrect
        "7",          #fridge usage- correct
        
        "",           #light bulb type
        
        "electrik",   #pump type- incorrect
        "electric",   #pump type- correct
        "nan",        #pump wattage- incorrect
        "2500",       #pump wattage- correct
        
        "electrik",   #oven type- incorrect
        "electric",   #oven type- correct
        "10",         #oven wattage- incorrect
        "100000",     #oven wattage- incorrect
        "5000 watts", #oven wattage- extra characters (acceptable)
        "30",         #oven usage- incorrect
        "1.5"        #oven usage- correct
        ])          
    
    def test_prompt_for_args_1(self, input):  
        self.house.prompt_for_args()
        print(str(self.house))
        print(self.house.get_consumption())
        print(self.house.get_max_current())
        
    '''
    test prompt_for_args() with a list of user input values. Use all defaults.
    '''
    @patch('eleclib.household.Household.get_input',side_effect=([""]*15))
    def test_prompt_for_args_2(self, input):          
        self.house.prompt_for_args()
        print(str(self.house))
        
class progTest(unittest.TestCase):
    
    def test_Oven(self):
        '''
        1. wattage, usage
        2. wattage
        3. usage
        4. none
        '''
        oven = Oven(4000,2)
        print(str(oven))
        
        oven = Oven(6000)
        print(str(oven))
        
        #test non-int usage as well
        oven = Oven(usage = 1.5)
        print(str(oven))
        
        #using defaults only
        oven = Oven()
        print(str(oven))
        
    def test_Fridge(self):
        '''
        1. wattage, unit=kwh/yr
        2. wattage, unit=watts, usage
        3. usage
        4. none
        '''
        
        fridge = Fridge(249, unit = 'kwh/yr')
        print(str(fridge))
        
        #try unit string from our list of alternatives (not 'watts')
        fridge = Fridge(450, 'watt', 6)
        print(str(fridge))
        
        fridge = Fridge(usage = 7)
        print(str(fridge))
        
        fridge = Fridge()
        print(str(fridge))
        
    def test_Lights(self):
        '''
        1. occupants, bulb_type, square_footage
        2. none
        '''
        lights = Lights('incandescent', 5, 1200)
        print(str(lights))
        
        lights = Lights()
        print(str(lights))
        
    def test_Heater(self):
        '''
        1.wattage, square_footage, R_walls, R_roof
        2.none
        '''
        heater = Heater(1500, 250, 24, 30)
        print(str(heater))
        
        heater = Heater()
        print(str(heater))
    
    def test_WaterHeater(self):
        '''
        1.wattage, occupants
        2.none
        '''
        water_heater = WaterHeater(3000, 4)
        print(str(water_heater))
        
        water_heater = WaterHeater()
        print(str(water_heater))
    
    def test_Pump(self):
        '''
        1.wattage, occupants
        2.none
        '''
        pump = Pump(3000, 4)
        print(str(pump))
        
        pump = Pump()
        print(str(pump))

    
def test_version():
    assert __version__ == '0.1.0'
    

if __name__ == '__main__':
    unittest.main()