#from unittest.mock import create_autospec
import unittest
from unittest.mock import patch
from eleclib import __version__
from eleclib.household import *

class cmdInputTest(unittest.TestCase):
    
    def setUp(self):
        self.house = Household()                    
        
    '''
    test prompt_square_footage with in-range, well-formatted input value
    resultant house.square_footage should then match the input
    '''
    @patch('eleclib.household.Household.get_input',return_value="10000")
    def test_prompt_square_footage_1(self, input):          
        self.house.prompt_square_footage()
        self.assertEqual(self.house.square_footage,10000)
        
    '''
    test prompt_square_footage with out of range value followed by a good input value 
    resultant house.square_footage should then match the second input.
    '''
    @patch('eleclib.household.Household.get_input',side_effect=["0","10000"])
    def test_prompt_square_footage_2(self, input):          
        self.house.prompt_square_footage()
        self.assertEqual(self.house.square_footage,10000)
        
    '''
    test prompt_square_footage in-range value but extra spaces added to the input
    '''
    @patch('eleclib.household.Household.get_input',return_value=" 10000")
    def test_prompt_square_footage_3(self, input):          
        self.house.prompt_square_footage()
        self.assertEqual(self.house.square_footage,10000)
        
    '''
    test prompt_square_footage in-range value but extra spaces added to the input
    '''
    @patch('eleclib.household.Household.get_input',return_value=" 10000 square feet")
    def test_prompt_square_footage_4(self, input):          
        self.house.prompt_square_footage()
        self.assertEqual(self.house.square_footage,10000)
        
        
def test_version():
    assert __version__ == '0.1.0'
    

if __name__ == '__main__':
    unittest.main()