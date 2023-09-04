class AircraftWB:
    
    unit_option = [ {"dist":"in", "weight":"lbs", "moment":"lbs/in", "capacity":"usg"}, 
                    {"dist":"ft", "weight":"lbs", "moment":"lbs/ft", "capacity":"usg"},
                    {"dist":"cm", "weight":"kg", "moment":"kg/cm" , "capacity":"litres"},
                    {"dist":"m", "weight":"kg", "moment":"kg/m", "capacity":"litres"}  ]
    fuel_types = ["Jet", "AvGas"]


       
    def __init__(self):
        self._units = dict()
        self._section_units = list()
        self._aircraft_type = "Test Type"
        self._fuel_type = "Jet"
        self._ac_weight_data = [{"true_weight":0.0, "true_moment":0.0, "mzfw":0.0, "mtow":0.0}]
        self._fuel_tanks = list()
        self._pax_sections = list()
        self._cargo_sections = list()
        self._forward_limit = 0.0
        self._aft_limit = 0.0

    
    def __del__(self):
        pass
    
    
    def __str__(self):
        return f"This is {self._aircraft_type} object"
        
    
    def set_unit_option(self, opt):
        try:
            opt = int(opt)
        except (ValueError, TypeError):
            return ValueError
        else:
            if opt >= 0 and opt <= 3:
                self._units = AircraftWB.unit_option[opt].copy()
            else:
                return IndexError
    
    
    def get_unit_option(self):
        return self._units
    
    
    @property
    def aircraft_type(self):
        return self._aircraft_type

    
    @aircraft_type.setter
    def aircraft_type(self, type_name):
        self._aircraft_type = type_name

        
    @property
    def fuel_type(self):
        return self._fuel_type

        
    @fuel_type.setter
    def fuel_type(self, fuel_type_index):
        try:
            fuel_type_index = int(fuel_type_index)
        except (ValueError, TypeError):
            return ValueError
        else:
            if fuel_type_index >= 0 and fuel_type_index <= 1:
                self._fuel_type = AircraftWB.fuel_types[fuel_type_index]
            else:
                return IndexError

    
    @property
    def section_units(self):
        return self._section_units
    
    
    @section_units.setter
    def section_units(self, val):
        self._section_units.append(val)
     
     
    @section_units.deleter
    def section_units(self):
        self._section_units.clear()


    def set_aircraft_weight_data(self, oew, oew_m, mzfw, mtow):
        try:
            oew = round(float(oew), 2)
            oew_m = round(float(oew_m), 2)
            mzfw = round(float(mzfw), 2)
            mtow = round(float(mtow), 2)
        except (ValueError, TypeError):
            return ValueError
        else:
            if oew < mzfw and mzfw <= mtow:
                self._ac_weight_data.clear()
                self._ac_weight_data = [{"true_weight":oew, "true_moment":oew_m, "mzfw":mzfw, "mtow":mtow}]
            else:
                return ValueError
            
    
    def get_aircraft_weight_data(self):
        return self._ac_weight_data
    
    
    @property
    def forward_cg_limit(self):
        return self._forward_limit

        
    @forward_cg_limit.setter
    def forward_cg_limit(self, fwd_lim):
        try:
            self._forward_limit = round(float(fwd_lim), 2)
        except (ValueError, typeError):
            return False
    
    
    @property
    def aft_cg_limit(self):
        return self._aft_limit
        
        
    @aft_cg_limit.setter
    def aft_cg_limit(self, aft_lim):
        try:
            self._aft_limit = round(float(aft_lim), 2)
        except (ValueError, TypeError):
            return False
    
    
    def add_fuel_tank(self, max_cap, max_fuel_moment, mult):
        try:
            max_cap = float(max_cap)
            max_fuel_moment = float(max_fuel_moment)
        except (ValueError, TypeError):
            return ValueError
        else:
            if max_cap > 0.0:
                max_fuel_weight = round(self.convert_fuel_to_weight(max_cap), 2)
                max_fuel_moment = round((lambda: max_fuel_moment, lambda: max_fuel_weight * max_fuel_moment)[mult](), 2)
                self._fuel_tanks.append({"max_fuel_cap":max_cap, "max_weight": max_fuel_weight, "max_moment":max_fuel_moment, "true_fuel_cap":0.0, "true_weight":0.0, "true_moment":0.0})
            else:
                return ValueError


    def delete_fuel_tank(self, tank_index):
        try:
            tank_index = int(tank_index)
        except (ValueError, TypeError):
            return ValueError
        else:
            if tank_index < len(self._fuel_tanks) and tank_index >= 0 and len(self._fuel_tanks) > 0:
                del self._fuel_tanks[tank_index]
            else:
                return IndexError
                
        
    def get_fuel_tank(self, tank_index):
        try:
            tank_index = int(tank_index)
        except (ValueError, TypeError):
            return ValueError
        else:
            if tank_index < len(self._fuel_tanks) and tank_index >= 0 and len(self._fuel_tanks) > 0:
                return self._fuel_tanks[tank_index]
            else:
                return IndexError


    def set_fuel_tank(self, tank_index, quantity):
        try:
            tank_index = int(tank_index)
            quantity = round(float(quantity), 2)
        except (ValueError, TypeError):
            return ValueError
        else:
            if tank_index < len(self._fuel_tanks) and tank_index >= 0 and len(self._fuel_tanks) > 0:
                if quantity >= 0.0 and quantity <= self._fuel_tanks[tank_index]["max_fuel_cap"]:
                    fuel_weight = self.convert_fuel_to_weight(quantity)
                    self._fuel_tanks[tank_index]["true_weight"] = fuel_weight
                    self._fuel_tanks[tank_index]["true_fuel_cap"] = quantity
                    mfw = self._fuel_tanks[tank_index]["max_weight"]
                    mfm = self._fuel_tanks[tank_index]["max_moment"]
                    self._fuel_tanks[tank_index]["true_moment"] = self.moment_interpolator(mfw, fuel_weight, mfm)
                else:
                    return ValueError
            else:
                return IndexError

                
    def convert_fuel_to_weight(self, capacity):
        try:
            capacity = float(capacity)
        except (ValueError, TypeError):
            return ValueError
        else:
            if self._fuel_type == "Jet":
                if self._units["capacity"] == "usg":
                    # USG to POUNDS (Jet A)
                    fuel_weight = capacity * 6.7
                else:
                    # LITRES to KILOGRAMS (Jet A)
                    fuel_weight = capacity * 0.803
            else:
                if self._units["capacity"] == "usg":
                    # USG to POUNDS (AvGas)
                    fuel_weight = capacity * 6.0
                else:
                    # LITRES to KILOGRAMS (AvGas)
                    fuel_weight = capacity * 0.719
            return round(fuel_weight, 2)

    
    def add_pax_section(self, max_pax_weight, max_pax_moment, mult):
        try:
            max_pax_weight = round(float(max_pax_weight), 2)
            max_pax_moment = float(max_pax_moment)
        except (ValueError, TypeError):
            return ValueError
        else:
            if max_pax_weight > 0.0:
                max_pax_moment = round((lambda: max_pax_moment, lambda: max_pax_weight * max_pax_moment)[mult](), 2)
                max_pax_number = self.convert_weight_to_pax(max_pax_weight)
                self._pax_sections.append({"max_pax_number":max_pax_number, "max_weight":max_pax_weight, "max_moment":max_pax_moment, "true_pax_number":0, "true_weight":0, "true_moment":0.0, })
            else: 
                return ValueError
    
    
    def delete_pax_section(self, pax_index):
        try:
            pax_index = int(pax_index)
        except (ValueError, TypeError):
            return ValueError
        else:
            if len(self._pax_sections) > 0:
                if pax_index < len(self._pax_sections) and pax_index >= 0: # and len(self._pax_sections) > 0:
                    del self._pax_sections[pax_index]
                else:
                    return IndexError
            else:
                return IndexError
                
    
    def get_pax_section(self, pax_index):
        try:
            pax_index = int(pax_index)
        except (ValueError, TypeError):
            return ValueError
        else:
            if len(self._pax_sections) > 0:
                if pax_index < len(self._pax_sections) and pax_index >= 0: # and len(self._pax_sections) > 0:
                    return self._pax_sections[pax_index]
                else:
                    return IndexError
            else:
                return IndexError

    
    def set_pax_section(self, pax_index, pax_number):
        try:
            pax_index = int(pax_index)
            pax_number = int(pax_number)
        except (ValueError, TypeError):
            return ValueError
        else:
            if len(self._pax_sections) > 0:
                if pax_index < len(self._pax_sections) and pax_index >= 0:
                    if pax_number >= 0 and pax_number <= self._pax_sections[pax_index]["max_pax_number"]:
                        pax_weight = self.convert_pax_to_weight(pax_number)
                        self._pax_sections[pax_index]["true_weight"] = pax_weight
                        self._pax_sections[pax_index]["true_pax_number"] = pax_number
                        mpw = self._pax_sections[pax_index]["max_weight"]
                        mpm = self._pax_sections[pax_index]["max_moment"]
                        self._pax_sections[pax_index]["true_moment"] = self.moment_interpolator(mpw, pax_weight, mpm)
                    else:
                        return ValueError
                else:
                    return IndexError
            else:
                return IndexError

    
    def convert_pax_to_weight(self, pax_number):
        try:
            pax_number = int(pax_number)
        except (ValueError, TypeError):
            return ValueError
        else:
            if self._units["weight"] == "lbs":
                pax_weight = pax_number * 190
            else:
                pax_weight = pax_number * 86
            return round(pax_weight, 2)


    def convert_weight_to_pax(self, pax_weight):
        try:
            pax_weight = float(pax_weight)
        except (ValueError, TypeError):
            return ValueError
        else:
            if self._units["weight"] == "lbs":
                pax_number = pax_weight / 190
            else:
                pax_number = pax_weight / 86
            # No need to round, will always be an integer.
            return int(pax_number)

     
    def add_cargo_section(self, max_cargo_weight, max_cargo_moment, mult):
        try:
            max_cargo_weight = round(float(max_cargo_weight), 2)
            max_cargo_moment = float(max_cargo_moment)
        except (ValueError, TypeError):
            return ValueError
        else:
            if max_cargo_weight > 0.0:
                max_cargo_moment = round((lambda: max_cargo_moment, lambda: max_cargo_weight * max_cargo_moment)[mult](), 2)
                self._cargo_sections.append({"max_weight":max_cargo_weight, "max_moment":max_cargo_moment, "true_weight":0.0, "true_moment":0.0})
            else:
                return ValueError
            

    def delete_cargo_section(self, cargo_index):
        try:
            cargo_index = int(cargo_index)
        except (ValueError, TypeError):
            return ValueError
        else:
            if len(self._cargo_sections) > 0:
                if cargo_index < len(self._cargo_sections) and cargo_index >=0:
                    del self._cargo_sections[cargo_index]
                else:
                    return IndexError
            else:
                return IndexError

    
    def get_cargo_section(self, cargo_index):
        try:
            cargo_index = int(cargo_index)
        except (ValueError, TypeError):
            return ValueError
        else:
            if len(self._cargo_sections) > 0:
                if cargo_index < len(self._cargo_sections) and cargo_index >=0: # and len(self._cargo_sections) > 0:
                    return self._cargo_sections[cargo_index]
                else:
                    return IndexError
            else:
                return IndexError

            
    def set_cargo_section(self, cargo_index, cargo_weight):
        try:
            cargo_index = int(cargo_index)
            cargo_weight = round(float(cargo_weight), 2)
        except (ValueError, TypeError):
            return ValueError
        else:
            if len(self._cargo_sections) > 0:
                if cargo_index < len(self._cargo_sections) and cargo_index >= 0: # and len(self._cargo_sections) > 0: 
                    if cargo_weight >= 0.0 and cargo_weight <= self._cargo_sections[cargo_index]["max_weight"]:
                        self._cargo_sections[cargo_index]["true_weight"] = cargo_weight
                        mcw = self._cargo_sections[cargo_index]["max_weight"]
                        mcm = self._cargo_sections[cargo_index]["max_moment"]
                        self._cargo_sections[cargo_index]["true_moment"] = self.moment_interpolator(mcw, cargo_weight, mcm)
                    else:
                        return ValueError
                else:
                    return IndexError
            else:
                return IndexError
            
    
    def moment_interpolator(self, max_weight, weight, max_moment):
        try:
            max_weight = float(max_weight)
            weight = float(weight)
            max_moment = float(max_moment)
        except (TypeError, ValueError):
            return ValueError
        else:
            try:
                moment = round((weight / max_weight) * max_moment, 2)
            except ZeroDivisionError:
                return ZeroDivisionError
            else:
                return moment
        