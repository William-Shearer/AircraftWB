from acwbclass import AircraftWB
import sys
from os import name, getcwd, listdir, system
from pandas import DataFrame
import pickle
from re import search
from copy import deepcopy

# Global stuff...

func_set_list = list()
create_text = ["CAPACITY", "LOAD", "LOAD", "FUEL TANK", "CREW/PAX SECTION", "CARGO SECTION"]
# section_units = list()
# var_list = list()
# dset = list()
# dind = list()


def main():
    acwb = None
    
    while True:
        clear_screen(name)
        print(print_main_menu())
        while True:
            if (sel := menu_selector(1, 5)) != False:
                break
            
        if sel == 1:
            # Create a new aircraft
            acwb = create_aircraft()
            # data_set, data_index = construct_data_set(acwb)
            # data_display = DataFrame(data_set, index = data_index)
            # print(data_display)
            show_aircraft(acwb)
            hit_enter()
            
        elif sel == 2:
            # Load a saved aircraft
            if (fl := get_file_list()) != False:
                clear_screen(name)
                print("\nSELECT AIRCRAFT TO LOAD")
                [print((i + 1),".\t".expandtabs(3), f, "\n", sep = "", end = "") for i, f in enumerate(fl)]
                if (sel := menu_selector(1, len(fl))) != False:
                    input_file = fl[sel - 1]
                    
                    with open(input_file, "rb") as aircraft_file:
                        acwb = pickle.load(aircraft_file)
                    show_aircraft(acwb)
                    hit_enter()
                else:
                    hit_enter()
            else:
                print("\nNo stored aircraft to load.")
                hit_enter()
                
        elif sel == 3:
            # Save Aircraft
            # Zero weight data in aircraft to be saved.
            temp_acwb = clear_weights(acwb)
            # Already done in clear_weights, now.
            #if isinstance(temp_acwb, AircraftWB):
            if temp_acwb != None:
                file_name = temp_acwb.aircraft_type
                with open(fr"{file_name}.acf", "wb") as aircraft_file:
                    pickle.dump(temp_acwb, aircraft_file)
                print("\nAircraft saved.")
            else:
                print("\nNo aircraft to save.\nPlease create an aircraft.")
            hit_enter()
            del temp_acwb
            
        elif sel == 4:
            # Set aircraft weights
            if isinstance(acwb, AircraftWB):
                set_aircraft(acwb)
                show_aircraft(acwb)
                # hit_enter()
            else:
                print("\nERROR: No aircraft to set and calculate.\nPlease create or load an aircraft.")
            hit_enter()
            
        elif sel == 5:
            # Exit program
            clear_screen(name)
            sys.exit("\nProgram terminated.\nThank you!\n")
            
        else:
            print(std_error_msg())
        
    """
    data_set, data_index = construct_data_set(acwb)
    data_display = DataFrame(data_set, index = data_index)
    print(data_display)
    """
 
 
def print_main_menu():
    return f"\nMAIN MENU\n1. Create New Aircraft\n2. Load Aircraft\n3. Save Aircraft\n4. Set and Calculate W&B\n5. Exit\n"
 
 
def menu_selector(lower, higher):
    try:
        selection = int(input("Selet Option: "))
    except (ValueError, TypeError):
        print(invalid_selection())
        return False
    else:
        if lower <= selection <= higher:
            return selection
        else:
            print(invalid_selection())
            return False


def get_file_list():
    path = fr"{getcwd()}"
    files = listdir(path)
    file_list = list()
    for file in files:
        try:
            if search(r"(\.[^.]+)", file.lower()).group(0) == ".acf":
                file_list.append(file)
        except AttributeError:
            pass
    if len(file_list) > 0:
        return file_list
    else:
        return False


def create_aircraft():
    func_create_list = list()
    func_delete_list = list()
    # class construction
    ac_class = AircraftWB()
    # create function variables to list
    func_create_list.append(ac_class.add_fuel_tank)
    func_create_list.append(ac_class.add_pax_section)
    func_create_list.append(ac_class.add_cargo_section)
    # set function variables to list
    func_delete_list.append(ac_class.delete_fuel_tank)
    func_delete_list.append(ac_class.delete_pax_section)
    func_delete_list.append(ac_class.delete_cargo_section)
    clear_screen(name)
    # Create aircraft type
    print("\nCREATE AIRCRAFT TYPE")
    ac_class.aircraft_type = input("Enter aircraft type (model): ")
    
    while True:
        if define_unit_option(ac_class):
            break
        else:
            print(invalid_selection())
            hit_enter()
            
    while True:
        if define_fuel_option(ac_class):
            break
        else:
            print(invalid_selection())
            hit_enter()
            
    while True:
        if define_basic_weights(ac_class, ac_class.get_unit_option()):
            break
        else:
            print(std_error_msg())
            hit_enter()

    while True:
        clear_screen(name)
        for i in range(3):
            print(f"\nSET NUMBER OF {create_text[i + 3]}S")
            while True:
                try:
                    num = int(input(f"Enter number: "))
                except (ValueError, TypeError):
                    print(std_error_msg())
                else:
                    if num >= 0:
                        ac_class.section_units = num
                        break
                    else:
                        print("\nERROR: Negative numbers, please try again.\n")
                        hit_enter()
        if yes_no("\nIs this correct? (Y or N): "):
            print()
            break
        else:
            del ac_class.section_units
                        
    
    for phase in range(3):
        clear_screen(name)
        print(f"\nCREATE {create_text[phase + 3]}S")
        for section_id in range(ac_class.section_units[phase]):
            while True:
                if create_sections(phase, func_create_list[phase], section_id, ac_class.get_unit_option()):
                    print(f"\n{create_text[phase + 3]} No.{(section_id + 1)} created successfully.\n")
                    if yes_no("Is this correct? (Y or N): "):
                        print()
                        break
                    else:
                        func_delete_list[phase](section_id)
                        print("Please correct the error...\n")
                else:
                    print(std_error_msg())
            # hit_enter()
            
    
    while True:
        clear_screen(name)
        print(f"\nSET CG LIMITS")
        try:
            ac_class.forward_cg_limit = float(input(f"Enter forward CG limit ({ac_class.get_unit_option()['dist']}): "))
            ac_class.aft_cg_limit = float(input(f"Enter aft CG limit ({ac_class.get_unit_option()['dist']}):  "))
        except (ValueError, TypeError):
            print(std_error_msg())
        else:
            if ac_class.forward_cg_limit < ac_class.aft_cg_limit:
                if yes_no("\nIs this correct? (Y or N): "):
                    break
            else:
                print("\nERROR: Fwd Limit > Aft Limit\n")
                hit_enter()
    
    func_create_list.clear()
    func_delete_list.clear()
    
    return deepcopy(ac_class)


def set_aircraft(ac_class):
    func_set_list = list()
    # set function variables to list
    func_set_list.append(ac_class.set_fuel_tank)
    func_set_list.append(ac_class.set_pax_section)
    func_set_list.append(ac_class.set_cargo_section)
    # phase is whether it is a tank, crew/pax section, or cargo section. Don't sweat it!
    for phase in range(3):
        clear_screen(name)
        print(f"\nSET {create_text[phase + 3]}S")
        # section_id is just the retreived number of units in each phase, stored in section_units list.
        for section_id in range(ac_class.section_units[phase]):
            while True:
                if set_sections(phase, func_set_list[phase], section_id, ac_class.get_unit_option()):
                    print(f"\n{create_text[phase + 3]} No.{(section_id + 1)} was set successfully.\n")
                    if yes_no("Is this correct? (Y or N): "):
                        break
                    print()
                else:
                    print(std_error_msg())
            #hit_enter()
    
    func_set_list.clear()


def define_unit_option(ac_class):
    clear_screen(name)
    print("\nSELECT UNIT OPTION")
    for i, each in enumerate(AircraftWB.unit_option):
        print(i + 1, end = "\t".expandtabs(3))
        for value in each:
            print(each[value], end = "\t".expandtabs(2))
        print()
    opt = input("\nOption: ").strip()
    try:
        opt = int(opt) - 1
    except (ValueError, TypeError):
        return False
    else:
        failure = ac_class.set_unit_option(opt)
        if failure == IndexError or failure == ValueError:
            return False
        else:
            return True


def define_fuel_option(ac_class):
    clear_screen(name)
    print("\nSELECT FUEL OPTION")
    for i, each in enumerate(AircraftWB.fuel_types):
        print((i + 1), f"\t{each}".expandtabs(2))
    try:
        opt = int(input("\nOption: ")) - 1
    except (ValueError, TypeError):
        return False
    else:
        if 1 >= opt >= 0:
            ac_class.fuel_type = opt
            return True
        else:
            return False
        

def define_basic_weights(ac_class, units):
    while True:
        clear_screen(name)
        print("\nAIRCRAFT BASIC WEIGHT DATA")
        print(f"Enter WEIGHT in ({units['weight']}) and MOMENT in ({units['moment']}).")
        oew = input("Enter Basic Empty Weight: ")
        oew_max_moment = input("Enter Basic Empty Moment: ")
        mzfw = input("Enter Maximum Zero Fuel Weight: ")
        mtow = input("Enter Maximum Take Off Weight: ")
        if yes_no("\nIs this correct? (Y or N): "):
            break
    if ac_class.set_aircraft_weight_data(oew, oew_max_moment, mzfw, mtow) == ValueError:
        return False
    else:
        if ac_class.get_aircraft_weight_data()[0]["mtow"] >= ac_class.get_aircraft_weight_data()[0]["mzfw"] > ac_class.get_aircraft_weight_data()[0]["true_weight"]:
            return True
        else:
            return False
        
        
def create_sections(phase, func, sec_id, units):
    if phase == 0:
        unit = units["capacity"]
    else:
        unit = units["weight"]
    print(f"Enter MAX {create_text[phase]} ({unit}) and MAX MOMENT ({units['moment']}) for {create_text[phase + 3]} No.{(sec_id + 1)}, separated by space.")
    data = input("Enter data: ").strip().split()
    if len(data) == 2:
        # if func_create_list[phase](data[0], data[1], False) == ValueError:
        if func(data[0], data[1], False) == ValueError:
            return False
        else:
            return True
    elif len(data) == 3:
        if data[1].upper() == "X":
            # if func_create_list[phase](data[0], data[2], True) == ValueError:
            if func(data[0], data[2], True) == ValueError:
                return False
            else:
                return True
    else:
        # Catch all
        return False
        

def set_sections(phase, func, sec_id, units):
    if phase == 0:
        unit = units["capacity"]
    elif phase == 1:
        unit = "number of CREW/PAX"
    else:
        unit = units["weight"]
    print(f"Enter REAL {create_text[phase]} ({unit}) for {create_text[phase + 3]} No.{(sec_id + 1)}.")
    data = input("Enter data: ")
    # if func_set_list[phase](sec_id, data) == ValueError:
    if func(sec_id, data) == ValueError:
        return False
    else:
        return True
    

def construct_data_set(ac_class):
    if isinstance(ac_class, AircraftWB):
        dset = list()
        dind = list()
        var_list = list()
        sum_weights = 0.0
        sum_moments = 0.0
        var_list.append(ac_class._fuel_tanks)
        var_list.append(ac_class._pax_sections)
        var_list.append(ac_class._cargo_sections)
        dset.append({"MAX_WEIGHT":"-", "MAX_MOMENT":"-", "REAL_WEIGHT":ac_class.get_aircraft_weight_data()[0]["true_weight"], "REAL_MOMENT":ac_class.get_aircraft_weight_data()[0]["true_moment"]})
        dind.append(ac_class.aircraft_type)
        sum_weights += ac_class.get_aircraft_weight_data()[0]["true_weight"]
        sum_moments += ac_class.get_aircraft_weight_data()[0]["true_moment"]
        for i in range(3):
            for item in var_list[i]:
                dset.append({"MAX_WEIGHT":item["max_weight"], "MAX_MOMENT":item["max_moment"], "REAL_WEIGHT":item["true_weight"], "REAL_MOMENT":item["true_moment"]})
                sum_weights += item["true_weight"]
                sum_moments += item["true_moment"]
                dind.append(create_text[i + 3])
            
        dset.append({"MAX_WEIGHT":"-", "MAX_MOMENT":"-", "REAL_WEIGHT":sum_weights, "REAL_MOMENT":sum_moments})
        dind.append("TOTAL REAL")
        return dset.copy(), dind.copy(), sum_weights, sum_moments
    else:
        return False


def calculate_CG(sum_moments, sum_weights):
    if sum_weights != 0.0:
        return round((sum_moments / sum_weights), 2)
    else:
        raise ZeroDivisionError


def show_aircraft(ac_class):
    if isinstance(ac_class, AircraftWB):
        data_set, data_index, sw, sm = construct_data_set(ac_class)
        data_display = DataFrame(data_set, index = data_index)
        clear_screen(name)
        print(f"\nAircraft Type:       {ac_class.aircraft_type}")
        print(f"Standard Units:      ", end = "")
        [print(u, end = " ") for u in ac_class.get_unit_option().values()]
        print(f"\nFuel Type:           {ac_class.fuel_type}")
        print(f"MTOW / MZFW:         {ac_class.get_aircraft_weight_data()[0]['mtow']} / {ac_class.get_aircraft_weight_data()[0]['mzfw']}")
        print(f"Fwd / Aft CG Limits: {ac_class.forward_cg_limit} / {ac_class.aft_cg_limit}\n")
        print("SECTION WEIGHT DATA")
        print(data_display, end = "\n\n")
        print("NOTES:")
        cg_pos = calculate_CG(sm, sw)
        print(f"CG position:          {cg_pos}")
        if cg_pos < ac_class.forward_cg_limit or cg_pos > ac_class.aft_cg_limit:
            print("** WARNING: AIRCRAFT IS OUT OF CG LIMITS ***")
        if sw > ac_class.get_aircraft_weight_data()[0]['mtow']:
            print("** WARNING: AIRCRAFT IS OVER MTOW **")
        fw = 0
        for i in range(ac_class.section_units[0]):
            fw += ac_class.get_fuel_tank(i)["true_weight"]
        if (sw - fw) > ac_class.get_aircraft_weight_data()[0]['mzfw']:
            print("** WARNING: ZFW EXCEEDED **")
        print()
        return True
    else:
        return False
    
    
def clear_screen(osn):
    """
    clear_screen() clears screen depending on os.name
    """
    if osn == "nt":
        system("cls")
    elif osn == "posix":
        system("clear")
    else:
        raise SystemError("FATAL ERROR: Unable to clear screen.")
    print("AIRCRAFT WEIGHT AND BALANCE CALCULATOR")


def clear_weights(ac_class):
    if isinstance(ac_class, AircraftWB):
        temp_ac_class = deepcopy(ac_class)
        func_set_list = list()
        func_set_list.append(temp_ac_class.set_fuel_tank)
        func_set_list.append(temp_ac_class.set_pax_section)
        func_set_list.append(temp_ac_class.set_cargo_section)
        
        for phase in range(3):
            for section_id in range(temp_ac_class.section_units[phase]):
                # Zero is zero in any alnguage, no fancy stuff here.
                func_set_list[phase](section_id, 0.0)
        
        return temp_ac_class
    else:
        return None
        

def yes_no(msg):
    if input(msg).upper() == "Y":
        return True
    else:
        return False    
    
    
def std_error_msg():
    return "\nERROR: Please check data and try again.\n"
    

def invalid_selection():
    return "\nERROR: Please select a valid option.\n"
    

def hit_enter():
    input("Hit Enter to continue...\n")
    return True
 
 
if __name__ == "__main__":
    main()