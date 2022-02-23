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
        "electrik",   #oven type- incorrect
        "electric",   #oven type- correct
        "10",         #oven wattage- incorrect
        "100000",     #oven wattage- incorrect
        "5000 watts", #oven wattage- extra characters (acceptable)
        "gass",       #heating type- incorrect
        "gas",        #heating type- correct
        "electrik",   #water heater type- incorrect
        "electric",   #water heater type- correct
        "electrik",   #fridge type- incorrect
        "electric",   #fridge type- correct
        "10",         #fridge wattage- incorrect
        "100000",     #fridge wattage- incorrect
        "250 watts",  #fridge wattage- convert from watts to kwh/yr(acceptable)
        "",           #light bulb type
        "",           #roof insulation R-value
        ""])          #wall insulation R-value
    def test_prompt_for_args_1(self, input):          
        self.house.prompt_for_args()
        print(str(self.house))
        
    '''
    test prompt_for_args() with a list of user input values. Use all defaults.
    '''
    @patch('eleclib.household.Household.get_input',side_effect=([""]*10))
    def test_prompt_for_args_2(self, input):          
        self.house.prompt_for_args()
        print(str(self.house))
        
        
def test_version():
    assert __version__ == '0.1.0'
    

if __name__ == '__main__':
    unittest.main()