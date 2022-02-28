'''
Define a household to determine current and wattage loads, but also
hold positional data and GIS information for calculating the viability
of off-grid energies, etc.
'''
from eleclib.household import Household

class Property:
    '''
    =====================
    class Property
    =====================
    household, 
    location (country, city, coords),
    
    
    '''
    def __init__(self, **kwargs):
        
        if 'household' in kwargs:
            self.set_household(kwargs['household'])
        else:
            self.household = Household()
            
        if 'country', 'city' ,...:
            self.setLocation()...
            
        if 'water_source' in kwargs:
            ...
        
        
            
    def get_solar_productivity(self):
        
    def get_wind_productivity(self):
        
    def get_water_production(self):
        
    def get_solution(self, cost:int , grid-tied: bool,
                     wind: bool, solar: bool, water: bool)
        
        
    
class WaterSource:
    '''
    =====================
    class WaterSource
    =====================
    define a water source by flow rate, total drop (as available)
    define as seasonal or year round... how do we define a function
    for the year round productivity?
    methods 
        get_production() returns wattage
        
    '''
    
    def __init__(self, **kwargs):
        
        if 'flow' in kwargs:
            self.set_flowrate(kwargs['flow'])
            
        if 'drop' in kwargs:
            ...
            
    def get_production(self):
        
        
class PowerSolution:
    '''
    =====================
    class PowerSolution
    =====================
    define a power solution as a way of producing the required load to 
    support the defined household. This could be a single type of off-grid
    power or fully grid-tied or a combo of multiple producers...
    It will define the specifications for each power type, ie.
    wind turbine size (wattage), solar wattage (and number of panels),
    percentage of waterSource utilized, etc.
    
    inputs:
        use_water: bool
        use_wind: bool
        use_solar: bool
        use_grid: bool
        
        water_percentage: int #amount of the water source that can be used
        wind_max_power: int #max wattage from wind
        solar_space_sf: (int, int) #square footage of space for solar(unshaded)
        
        budget: int #define max cost for the off-grid setup?
        
    methods:
        get_solar()
        get_wind()
        get_water()
        get_grid()
        report_productions() #display or store to file the breakdown
            of cost and power production for each category...
        
    '''
    
class OffGridSolution:
    '''
    =====================
    class OffGridSolution
    =====================
    define an off grid solution by total power production.
    is it consistent like with water and usually wind or is it
    less productive in winter like solar?
    input: property, cost, production
    type: E{'solar','wind','water'}
    
    '''
    
class SolarSolution(OffGridSolution):
    '''
    =====================
    class SolarSolution
    =====================
    solar solution defines an OffGridSolution using solar energy,
    can be defined by production and calculate the nuber of panels,
    batteries, cost, et. or by cost and create the max power output
    for that cost... can be constrained to a specific voltage, and
    to a required output voltage... is this stored in household 
    (12,120,240V)?
    gets solar_roductivity from property object
    
    '''
    
class WindSolution(OffGridSolution):
    '''
    =====================
    class WindSolution
    =====================
    defines an off grid solution for wind. likely wattage constrained
    (relates closely to size and noise- can we define these instead?)
    else cost constrained
    gets wind productivity from property object
    '''
    
class WaterSolution(OffGridSolution):
    '''
    =====================
    class WaterSolution
    =====================
    defines a stream/dam based off grid solution. usually constrained
    mostly by the water source rather than cost or wattage
    '''