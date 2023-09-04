import unittest
from acwbclass import AircraftWB
from project import clear_screen
import contextlib


class Test_AircraftWB(unittest.TestCase):
    
    def setUp(self):
        self.acwb = AircraftWB()
        self.acwb.set_unit_option(0)
        self.acwb.aircraft_type = "T-41D"
        self.acwb.fuel_type = 1
        self.acwb.add_fuel_tank(23.0, 6486.0, False)
        self.acwb.add_fuel_tank(23.0, 6486.0, False)
        self.acwb.add_pax_section(400.0, 14000.0, False)
        self.acwb.add_pax_section(400.0, 28000, False)
        self.acwb.add_cargo_section(200, 18000.0, False)
        self.acwb.forward_cg_limit = 35.0
        self.acwb.aft_cg_limit = 47.0
        self.acwb.set_aircraft_weight_data(1510.0, 57000.0, 2500.0, 2500.0)        
     
    def tearDown(self):
        pass
    
    def test_aircraft_type(self):
        self.acwb.aircraft_type = "Cessna T-41D"
        self.assertEqual(self.acwb.aircraft_type, "Cessna T-41D")
    
    def test_set_unit_option(self):
        # Test that this actually does extract the respective dict object from the options.
        self.assertIsInstance(self.acwb._units, dict)
        # Make sure the self._units onject is independent of the class list of dicts unit_options.
        # It should be a copy of it.
        self.assertIsNot(self.acwb._units, AircraftWB.unit_option[0])
        # But do make sure that they say exactly the same thing...
        self.assertTrue(self.acwb._units, AircraftWB.unit_option[0])
        
    def test_get_unit_option(self):
        self.acwb.set_unit_option(3)
        test_dict = {"dist":"m", "weight":"kg", "moment":"kg/m", "capacity":"litres"}
        self.assertTrue(self.acwb.get_unit_option, test_dict)
        
    def test_fuel_type(self):
        self.acwb.fuel_type = 0
        self.assertEqual(self.acwb.fuel_type, "Jet")
        
    def test_section_units(self):
        # Test setter
        self.acwb.section_units = 2
        self.acwb.section_units = 2
        self.acwb.section_units = 1
        # Test getter
        self.assertEqual(self.acwb.section_units, [2, 2, 1])
        
    def test_set_aircraft_weight_data(self):
        self.acwb.set_aircraft_weight_data(1510.0, 57000.0, 2500.0, 2500.0)
        self.assertEqual(self.acwb._ac_weight_data, [{"true_weight":1510.0, "true_moment":57000.0, "mzfw":2500.0, "mtow":2500.0}])
    
    def test_get_aircraft_weight_data(self):
        self.acwb.set_aircraft_weight_data(1510.0, 57000.0, 2500.0, 2500.0)
        self.assertEqual(self.acwb.get_aircraft_weight_data()[0]["true_weight"], 1510.0)
        
    def test_add_fuel_tank(self):
        # add_fuel_tank is inherently tested because it is part of setUp()
        # It would not get this far if it failed, which is test enough.
        # Test that the tanks are a list of dictionaries, however.
        self.assertIsInstance(self.acwb._fuel_tanks, list)
        self.assertIsInstance(self.acwb._fuel_tanks[0], dict)
        self.assertIsInstance(self.acwb._fuel_tanks[1], dict)
        
    def test_delete_fuel_tank(self):
        # Test delete_fuel_tank
        self.acwb.delete_fuel_tank(1)
        self.assertTrue(len(self.acwb._fuel_tanks), 1)
        # Try and access a tank that does not exist, should handle and return an IndexError (not raise it)...
        self.assertEqual(self.acwb.get_fuel_tank(1), IndexError)
        self.assertEqual(self.acwb.set_fuel_tank(1, 20.0), IndexError)
        self.assertEqual(self.acwb.delete_fuel_tank(1), IndexError)
    
    def test_get_fuel_tank(self):
        # Set a correct dict template to test...
        fuel_test_dict = {"max_fuel_cap": 23.0, "max_weight": 138.0, "max_moment": 6486.0, "true_fuel_cap": 0.0, "true_weight":0.0, "true_moment": 0.0}
        self.assertEqual(self.acwb.get_fuel_tank(0), fuel_test_dict)
        self.assertEqual(self.acwb.get_fuel_tank(2), IndexError)
    
    def test_set_fuel_tank(self):
        # Test set_fuel_tank. Should return a dictionary, completely calculated.
        self.acwb.set_fuel_tank(0, 20)
        fuel_test_dict = {"max_fuel_cap": 23.0, "max_weight": 138.0, "max_moment": 6486.0, "true_fuel_cap": 20.0, "true_weight":120.0, "true_moment": 5640.0}
        self.assertEqual(self.acwb.get_fuel_tank(0), fuel_test_dict)
        # Test entering invalid data to a tank that does exist, should return a ValueError, not raise it...
        # Handles negatives
        self.assertEqual(self.acwb.set_fuel_tank(0, -20.0), ValueError)
        # Wrong type
        self.assertEqual(self.acwb.set_fuel_tank("zero", "one hundred"), ValueError)
        # Exceeds fuel weight limit
        self.assertEqual(self.acwb.set_fuel_tank(0, 200), ValueError)
        # Done.
    
    def test_convert_fuel_to_weight(self):
        # Test the converter...
        # US GALLONS with Jet and AvGas
        self.assertEqual(self.acwb.convert_fuel_to_weight(100.00), 600.00)
        self.acwb.fuel_type = 0
        self.assertEqual(self.acwb.convert_fuel_to_weight(100.00), 670.00)
        self.acwb.fuel_type = 1
        self.acwb.set_unit_option(2)
        # LITRES with Jet and AvGas
        self.assertEqual(self.acwb.convert_fuel_to_weight(100.00), 71.90)
        self.acwb.fuel_type = 0
        self.assertEqual(self.acwb.convert_fuel_to_weight(100.00), 80.30)
        self.acwb.fuel_type = 1
        self.acwb.set_unit_option(0)
        
    def test_add_pax_section(self):
        # add_pax_section is already tested in setUp(), or we would not be here...
        # Nonetheless, that it was created properly does need testing...
        self.assertIsInstance(self.acwb._pax_sections, list)
        self.assertIsInstance(self.acwb._pax_sections[0], dict)
        self.assertIsInstance(self.acwb._pax_sections[1], dict)
        
    def test_convert_pax_to_weight(self):
        # Test the convert_pax_to_weight
        # Pounds...
        self.assertEqual(self.acwb.convert_pax_to_weight(4), 760)
        # Kilograms...
        self.acwb.set_unit_option(2)
        self.assertEqual(self.acwb.convert_pax_to_weight(4), 344)
            
    def test_convert_weight_to_pax(self):
        # Test the convert_weight_to_pax function
        # Pounds...
        self.assertEqual(self.acwb.convert_weight_to_pax(760), 4)
        # Kilograms...
        self.acwb.set_unit_option(2)
        self.assertEqual(self.acwb.convert_weight_to_pax(344), 4)
            
    def test_set_pax_section(self):
        # Test set_pax_section
        self.acwb.set_pax_section(0, 2)
        self.acwb.set_pax_section(1, 1)
        # Create correct dicts for test template
        pax_test_dict0 = {"max_pax_number": 2, "max_weight": 400.0, "max_moment": 14000.0, "true_pax_number": 2, "true_weight": 380, "true_moment": 13300.0}
        pax_test_dict1 = {"max_pax_number": 2, "max_weight": 400.0, "max_moment": 28000.0, "true_pax_number": 1, "true_weight": 190, "true_moment": 13300.0}
        # Test get_pax_section
        self.assertEqual(self.acwb.get_pax_section(0), pax_test_dict0)
        self.assertEqual(self.acwb.get_pax_section(1), pax_test_dict1)
        # Try making a mistake with pax number...
        self.assertTrue(self.acwb.set_pax_section("one", "three"), ValueError)
        self.assertTrue(self.acwb.set_pax_section("one", 2), ValueError)
        self.assertTrue(self.acwb.set_pax_section(0, -1), ValueError)
        # Try to put too many pax in section 0 now. Should return a ValueError
        self.assertTrue(self.acwb.set_pax_section(0, 3), ValueError)
        
    
    def test_get_pax_section(self):
        # Create correct dicts for test template
        pax_test_dict0 = {"max_pax_number": 2, "max_weight": 400.0, "max_moment": 14000.0, "true_pax_number": 0, "true_weight": 0, "true_moment": 0}
        pax_test_dict1 = {"max_pax_number": 2, "max_weight": 400.0, "max_moment": 28000.0, "true_pax_number": 0, "true_weight": 0, "true_moment": 0}
        # Test get_pax_section
        self.assertEqual(self.acwb.get_pax_section(0), pax_test_dict0)
        self.assertEqual(self.acwb.get_pax_section(1), pax_test_dict1)
        # Test delete_pax_section
        self.acwb.delete_pax_section(0)
        # pax_section[0] should now be what pax_section[1] was, and pax_section[1] should not exist anymore
        self.assertEqual(self.acwb.get_pax_section(0), pax_test_dict1)
        # Try to access pax_section[1], which now does not exist. Should return an IndexError
        self.assertTrue(self.acwb.get_pax_section(1), IndexError)
         
    def test_add_cargo_section(self):
        # Test instances of _cargo_sections
        self.assertIsInstance(self.acwb._cargo_sections, list)
        self.assertIsInstance(self.acwb._cargo_sections[0], dict)
        # Test setting the cargo section
        self.acwb.set_cargo_section(0, 100)
        cargo_test_dict = {"max_weight": 200.0, "max_moment": 18000.0, "true_weight": 100.0, "true_moment": 9000.0}
        # Test get_cargo_section
        self.assertEqual(self.acwb.get_cargo_section(0), cargo_test_dict)
    
    def test_get_cargo_section(self):
        cargo_test_dict = {"max_weight": 200.0, "max_moment": 18000.0, "true_weight": 0.0, "true_moment": 0.0}
        # Test get_cargo_section
        self.assertEqual(self.acwb.get_cargo_section(0), cargo_test_dict)
        self.assertTrue(self.acwb.get_cargo_section(1), IndexError)
        
    def test_set_cargo_section(self):
        # Test setting the cargo section
        self.acwb.set_cargo_section(0, 100)
        cargo_test_dict = {"max_weight": 200.0, "max_moment": 18000.0, "true_weight": 100.0, "true_moment": 9000.0}
        # Test get_cargo_section
        self.assertEqual(self.acwb.get_cargo_section(0), cargo_test_dict)
        # Test out of ranges...
        self.assertTrue(self.acwb.set_cargo_section(1, 100.0), IndexError)
        self.assertTrue(self.acwb.set_cargo_section(-1, 100.0), IndexError)
        self.assertTrue(self.acwb.set_cargo_section(0, 300.0), ValueError)
        self.assertTrue(self.acwb.set_cargo_section(0, "one hundred pounds"), ValueError)
        self.assertTrue(self.acwb.set_cargo_section("zero", 200), ValueError)
        self.assertTrue(self.acwb.set_cargo_section(0, -100.0), ValueError)
        
    def test_delete_cargo_section(self):
        # Test delete_cargo_section
        self.acwb.delete_cargo_section(0)
        self.assertTrue(self.acwb.get_cargo_section(0), IndexError)
        
    def test_moment_interpolator(self):
        self.assertEqual(self.acwb.moment_interpolator(400.00, 200.00, 24000.00), 12000.0)
        self.assertTrue(self.acwb.moment_interpolator(0.0, 200.00, 24000.0), ZeroDivisionError)
        self.assertTrue(self.acwb.moment_interpolator(0.0, "two hundred", 24000.0), ValueError)
    
    def test_clear_screen(self):
        with contextlib.redirect_stdout(None):
            with self.assertRaises(SystemError) as context:
                clear_screen("no_sys")
            self.assertTrue("FATAL ERROR: Unable to clear screen." in str(context.exception))
            #self.assertIsNone(clear_screen("posix"))
            #self.assertIsNone(clear_screen("nt"))
    
if __name__ == "__main__":
    unittest.main()