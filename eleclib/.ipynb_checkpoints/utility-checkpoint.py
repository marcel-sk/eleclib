'''
extra utility functions not specific to another module
'''
from numbers import Number
from typing import List
UNITS = {'kwh/yr': 
             ['kwh/yr', 
              'kwh/year', 
              'kilowatt-hour/year', 
              'kilowatt hour per year', 
              'kilowatt-hour per year'],
        'watts': 
             ['watts', 
              'watt', 
              'w'],
         'watts/day': 
             ['watts/day', 
              'w/d', 
              'watt/day', 
              'watt/d', 
              'watts/d', 
              'w/day']
        }

def convert_to_watts(value: float, unit: str, usage: float = 8):
    if not usage:
        usage = 8
    assert type(unit)==str
    #if alt spelling is used convert to primary
    for key in UNITS:
        if unit in UNITS[key]:
            unit = key
    assert unit in UNITS
    assert isinstance(value, Number)
    assert isinstance(usage, Number)
    if unit == 'watts':
        return value
    elif unit == 'kwh/yr':
        return value*1000/(365*usage)
    elif unit == 'watts/day':
        return value*1000/365
    
def extract_number(text):
    digit_string = ""
    
    for char in text:
        if char.isdigit() or char == '.':
            digit_string += char
    if digit_string:
        number = float(digit_string)
        return number
    else:
        return False
    
def extract_unit(text):
    
    char_string = ""
    for char in text:
        if not char.isdigit():
            char_string += char
    char_string = char_string.strip()
    for key in UNITS:
        if char_string in UNITS[key]:
            char_string = key
    
    if char_string in UNITS:
        return char_string
    else:
        return 'watts'
        
def list_type(my_list: List, my_type: type):
    if isinstance(my_list, List):
        for element in my_list:
            if not isinstance(element, my_type):
                return False
        return True
    else:
        return False

def add_indent(text: str, indent: int = 4):
    lines = text.splitlines()
    indent = indent*' '
    newText = ""
    for line in lines:
        newText += indent + line + '\n'
    return newText