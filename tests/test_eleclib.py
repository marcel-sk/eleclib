from eleclib import __version__
from eleclib.household import *

house = Household(prompt=True)
print(house.get_power_usage())

def test_version():
    assert __version__ == '0.1.0'
    