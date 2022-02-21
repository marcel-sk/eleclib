DEFAULT_SQUARE_FOOTAGE = 6000
SQUARE_FOOTAGE_RANGE = [100,20000]

DEFAULT_HEATING_TYPE = "gas"
HEATING_TYPES = ["gas","wood","baseboard-electric","geo-electric","infloor-electric","none"]

DEFAULT_WATER_HEATER = "gas"
WATER_HEATER_TYPES = ["gas","electric","none"]
DEFAULT_WATER_HEATER_CAP = 50 #Gallons
WATER_HEATER_CAPACITY_RANGE = [3,200]

DEFAULT_OVEN_TYPE = "gas"
OVEN_TYPES = ["gas", "electric-full", "electric-toaster", "none"]
DEFAULT_OVEN_WATTAGE = 5000
OVEN_WATTAGE_RANGE = [1000-15000]
              
DEFAULT_BULB_TYPE = "LED"
LIGHT_BULB_TYPES = ["LED", "halogen", "incandescent"]

DEFAULT_FRIDGE_TYPE = "electric"
FRIDGE_TYPES = ["electric", "electic-low-volt", "propane", "propane-electric"]
DEFAULT_FRIDGE_WATTAGE_SPEC = "Kwh/yr"
WATTAGE_SPECS = ["Kwh/yr", "wh/day", "kwh/month", "running watts", "peak watts"]
#--THESE ARE IN KWH/YEAR--
DEFAULT_FRIDGE_WATTAGE = 400
DEFAULT_12V_FRIDGE_WATTAGE = 250
FRIDGE_WATTAGE_RANGE = [50,5000]

#R-VALUES BASED ON CURRENT BUILDING CODE VALUES FOR CANADA
DEFAULT_R_ROOF = 30
DEFAULT_R_WALLS = 24
R_RANGE = [0,100]

class Household:
    def __init__(self, 
        prompt = False,
        square_footage = DEFAULT_SQUARE_FOOTAGE, 
        heating_type = DEFAULT_HEATING_TYPE, 
        water_heater_type = DEFAULT_WATER_HEATER, 
        oven_type = DEFAULT_OVEN_TYPE,
        oven_wattage = 0,
        fridge_type = DEFAULT_FRIDGE_TYPE,
        fridge_wattage_spec = DEFAULT_FRIDGE_WATTAGE_SPEC,
        fridge_wattage = DEFAULT_FRIDGE_WATTAGE,
        light_bulbs = DEFAULT_BULB_TYPE, 
        R_roof = DEFAULT_R_ROOF, 
        R_walls = DEFAULT_R_WALLS,
        occupants = 3):
        
        if prompt:
            #set up state by interactive prompting
            self.prompt_for_args()
        else:
            #programmatic construction
            self.set_square_footage(square_footage)
            self.set_heating_type(heating_type)
            self.set_water_heater_type(water_heater_type)
            self.set_oven_type(oven_type)
            self.set_oven_wattage(oven_wattage)
            self.set_fridge_type(fridge_type)
            self.set_fridge_wattage_spec(fridge_wattage_spec)
            self.set_fridge_wattage(fridge_wattage)
            self.set_bulb_type(light_bulbs)
            self.set_R_roof(R_roof)
            self.set_R_walls(R_walls)
            self.set_occupants(occupants)
            
#--------------------------SETTER METHODS------------------------------------
        
    def set_square_footage(self,square_footage):
        #verify type
        if (type(square_footage) != int):
            return false
        
        #verify range
        min_val = SQUARE_FOOTAGE_RANGE[0]
        max_val = SQUARE_FOOTAGE_RANGE[1]
        if (square_footage and min_val<=square_footage<=max_val):
            self.square_footage = square_footage
            return True
        else:
            return False
        
    def set_heating_type(self, heating_type):
        self.heating_type = heating_type
        
    def set_water_heater_type(self, water_heater_type):
        self.water_heater_type = water_heater_type
            
    def set_oven_type(self, oven_type):
        if oven_type in OVEN_TYPES:
            self.oven_type = oven_type
            return True
        else:
            return False
        
    def set_oven_wattage(self, oven_wattage):
        assert(type(oven_wattage)==int)
        
        min_val = OVEN_WATTAGE_RANGE[0]
        max_val = OVEN_WATTAGE_RANGE[1]
        
        if min_val<=oven_wattage<=max_val:
            self.oven_wattage = oven_wattage
            return True
        else:
            return False
        
    def set_fridge_type(self, fridge_type):
        if fridge_type in FRIDGE_TYPES:
            self.fridge_type = fridge_type
            return True
        else:
            return False
        
        
    def set_fridge_wattage_spec(self, fridge_wattage_spec):
        if fridge_wattage_spec in WATTAGE_SPECS:
            self.fridge_wattage_spec = fridge_wattage_spec
            return True
        else:
            return False
        
    def set_fridge_wattage(self, fridge_wattage):
        assert(type(fridge_wattage)==int)
        
        min_val = FRIDGE_WATTAGE_RANGE[0]
        max_val = FRIDGE_WATTAGE_RANGE[1]
        
        if min_val<=fridge_wattage<=max_val:
            self.fridge_wattage = fridge_wattage
            return True
        else:
            return False
            
    def set_bulb_type(self, light_bulbs):
        if light_bulbs in LIGHT_BULB_TYPES:
            self.light_bulbs = light_bulbs
            return True
        else:
            return False
            
    def set_R_roof(self, R_roof):
        assert(type(R_roof)==int)
        
        min_val = R_RANGE[0]
        max_val = R_RANGE[1]
        
        if min_val<=R_roof<=max_val:
            self.R_roof = R_roof
            return True
        else:
            return False
            
    def set_R_walls(self, R_walls):
        assert(type(R_walls)==int)
        
        min_val = R_RANGE[0]
        max_val = R_RANGE[1]
        
        if min_val<=R_walls<=max_val:
            self.R_walls = R_walls
            return True
        else:
            return False
        
    def set_occupants(self, occupants):
        assert(type(occupants)==int)
        if 1 <= occupants <= 100:
            self.occupants = occupants
            return True
        return False
    
#------------------------------------
        
    def oven_is_electric(self):
        if (self.oven_type in OVEN_TYPES and self.oven_type in "electric"):
            return True
        else:
            return False
        
    def heating_is_electric(self):
        if (self.heating_type in HEATING_TYPES and self.heating_type in "electric"):
            return True
        else:
            return False
        
    def fridge_is_electric(self):
        if (self.fridge_type in FRIDGE_TYPES and self.fridge_type in "electric"):
            return True
        else:
            return False
        
#------------------PROMPTING FOR SETUP------------------------------------------
    
    def prompt_for_args(self):
        print("Creating new household...")
        print("Enter values specified or ENTER to use defaults")
        
        self.prompt_square_footage()
        self.prompt_oven_type()
        if self.oven_is_electric():
            self.promp_oven_wattage()
        self.prompt_heating_type()
        self.prompt_fridge_type()
        if self.fridge_is_electric():
            self.prompt_fridge_wattage()
        self.prompt_bulb_type()
        self.prompt_R_roof()
        self.prompt_R_walls()
        
    def prompt_square_footage(self):
        square_footage_raw = input("enter square footage (default: " + str(DEFAULT_SQUARE_FOOTAGE) + ") >")
        
        if not square_footage_raw:
            if self.set_square_footage(DEFAULT_SQUARE_FOOTAGE):
                return True
            else:
                return False
        
        else:
            square_footage = int(square_footage_raw)
            if self.set_square_footage(square_footage):
                return True
            else:
                print("Error: Input invalid!")
                min_val = SQUARE_FOOTAGE_RANGE[0]
                max_val = SQUARE_FOOTAGE_RANGE[1]
                print("should be an integer between ", min_val, " and ", max_val, " representing the total square footage of the house")
                self.prompt_square_footage()

 
    def prompt_oven_type(self):
        oven_type = input("enter oven type (default: " + DEFAULT_OVEN_TYPE + ") >")
                  
        #no entry, use default
        if not oven_type:
            if self.set_oven_type(DEFAULT_OVEN_TYPE):
                return True
            return False
        
        else:
            if self.set_oven_type(oven_type):
                return True
            else:
                print("Error: Input invalid!")
                print("should be one of ")
                for element in OVEN_TYPES:
                      print("   ",element, ",")
                self.prompt_oven_type()
                  
    def prompt_oven_wattage(self):
        oven_wattage = input("enter oven wattage (default: " + str(DEFAULT_OVEN_WATTAGE) + ") >")
        #no entry, use default
        if not oven_wattage:
            assert(self.oven_is_electric())
            if self.set_oven_wattage(DEFAULT_OVEN_WATTAGE):
                return True
            return False
                      
        else:
            if self.set_oven_wattage(oven_wattage):
                return True
            else:
                print("Error: Input invalid!")
                min_val = OVEN_WATTAGE_RANGE[0]
                max_val = OVEN_WATTAGE_RANGE[1]
                print("should be an integer between ", min_val, " and ", max_val, " representing the rated power in watts")
                self.prompt_oven_wattage()
        
    def prompt_heating_type(self):
        
        heating_type = input("enter heating type (default: " + DEFAULT_HEATING_TYPE + ") >")
                  
        #no entry, use default
        if not heating_type:
            if self.set_heating_type(DEFAULT_HEATING_TYPE):
                return True
            return False
        
        else:
            if self.set_heating_type(heating_type):
                return True
            else:
                print("Error: Input invalid!")
                print("should be one of ")
                for element in HEATING_TYPES:
                      print("   ",element, ",")
                self.prompt_heating_type()
        
    def prompt_fridge_type(self):
        
        fridge_type = input("enter fridge type (default: " + DEFAULT_FRIDGE_TYPE + ") >")
                  
        #no entry, use default
        if not fridge_type:
            if self.set_fridge_type(DEFAULT_FRIDGE_TYPE):
                return True
            return False
        
        else:
            if self.set_fridge_type(fridge_type):
                return True
            else:
                print("Error: Input invalid!")
                print("should be one of ")
                for element in FRIDGE_TYPES:
                      print("   ",element, ",")
                self.prompt_fridge_type()
                      
    def prompt_fridge_wattage(self):
        print("To enter value in running watts enter <### watts>")
        print("This will assume 8 running hrs/day")
        fridge_wattage_raw = input("enter fridge wattage (default: " + str(DEFAULT_FRIDGE_WATTAGE) + ") >")
                      
        #no entry, use default- different 120v vs 12v defaults
        if not fridge_wattage_raw:
            if self.fridge_type == "electric":
                fridge_wattage = DEFAULT_FRIDGE_WATTAGE
            elif (self.fridge_type == "electric-low-volt" or self.fridge_type == "propane-electric"):
                fridge_wattage = DEFAULT_12V_FRIDGE_WATTAGE
                      
        #watts entered to change unit used- convert by 8hrs running time/day
        elif fridge_wattage_raw in "watts":
            chars = ""
            for char in fridge_wattage_raw:
                if char.isdigit():
                      chars.append(char)
            wattage = int(chars)
            fridge_wattage = wattage*8*365/1000
            
        #input should be just a number (in string format)              
        else:
            try:
                fridge_wattage = int(fridge_wattage_raw)
            except:
                fridge_wattage = None
                
        if fridge_wattage and self.set_fridge_wattage(fridge_wattage):
            return True
        else:
            print("Error: Input invalid!")
            min_val = FRIDGE_WATTAGE_RANGE[0]
            max_val = FRIDGE_WATTAGE_RANGE[1]
            print("should be an integer between ", min_val, " and ", max_val, " representing the yearly Kwh consumption")
            self.prompt_fridge_wattage()
                      
                      
    def prompt_bulb_type(self):
        
        bulb_type = input("enter light bulb type (default: " + DEFAULT_BULB_TYPE + ") >")
                  
        #no entry, use default
        if not bulb_type:
            if self.set_bulb_type(DEFAULT_BULB_TYPE):
                return True
            return False
        
        else:
            if self.set_bulb_type(bulb_type):
                return True
            else:
                print("Error: Input invalid!")
                print("should be one of ")
                for element in LIGHT_BULB_TYPES:
                      print("   ",element, ",")
                self.prompt_bulb_type()
                      
    def prompt_R_roof(self):
        R_roof = input("enter roof insulation R-value (default: " + str(DEFAULT_R_ROOF) + ") >")
        #no entry, use default
        if not R_roof:
            if self.set_R_roof(DEFAULT_R_ROOF):
                return True
            return False
                      
        else:
            if self.set_R_roof(R_roof):
                return True
            else:
                print("Error: Input invalid!")
                min_val = R_RANGE[0]
                max_val = R_RANGE[1]
                print("should be an integer between ", min_val, " and ", max_val, " representing the R-value of insulation in the roof")
                self.prompt_R_roof()
        
    def prompt_R_walls(self):
        R_walls = input("enter wall insulation R-value (default: " + str(DEFAULT_R_WALLS) + ") >")
        #no entry, use default
        if not R_walls:
            if self.set_R_walls(DEFAULT_R_WALLS):
                return True
            return False
                      
        else:
            if self.set_R_walls(R_walls):
                return True
            else:
                print("Error: Input invalid!")
                min_val = R_RANGE[0]
                max_val = R_RANGE[1]
                print("should be an integer between ", min_val, " and ", max_val, " representing the R-value of insulation in the exterior walls")
                self.prompt_R_walls()
        
    #-------------------------------------ACCESSORS---------------------------------
    def get_power_usage(self):
        total_usage = (self.get_lighting_usage() +
            self.get_oven_usage() +
            self.get_heating_usage() +
            self.get_water_heater_usage() +
            self.get_pump_usage() +
            self.get_fridge_usage())/1000
        return total_usage
        
    
    def get_lighting_usage(self):
        #watts/day
        return(100)
    
    def get_oven_usage(self):
        if self.oven_is_electric():
            daily = self.oven_wattage*1
            return daily
        else:
            return(0)
    
    def get_heating_usage(self):
        return(0)
    
    def get_water_heater_usage(self):
        return(0)
    
    def get_pump_usage(self):
        return(200)
    
    def get_fridge_usage(self):
        daily = self.fridge_wattage*1000/365
        return(daily)
            
            
            
#--------------------------------REPORTING AND RECOMMENDATIONS-----------------------
    def get_recommendations(self):
        return False
    
    def report(format="xlsx"):
        return False
