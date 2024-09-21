#unit test file for the menu.py file

import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
import sys
import os
# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils

class TestMenu(unittest.TestCase):
    
        def setUp(self):
            # Create an instance of BikeDB and mock the database connection and cursor
            self.menu = utils.MenuUtils()
    
        # see if the menu is an instance of MenuUtils
        def test_menu_instance(self):
            self.assertIsInstance(self.menu, utils.MenuUtils)
        
        # mimic user input and compare to expected output
        @patch('builtins.input', side_effect=['1', '2'])
        def test_user_input(self, mock_input):
            result = self.menu.get_user_input()
            print(result)
            self.assertEqual(self.menu.get_user_input_values(), [1, 2])

        # mimic user input and compare to expected output
        @patch('builtins.input', side_effect=['0', '0'])
        def test_user_input_string(self, mock_input):
            result = self.menu.get_user_input()
            print(result)
            print(self.menu.convert_val_to_name())
            self.assertEqual(self.menu.convert_val_to_name(), ['Bike_db', 'view'])
        
         # mimic user input and compare to expected output
        @patch('builtins.input', side_effect=['0', '5', '1','1'])
        def test_user_input_string(self, mock_input):
            result = self.menu.get_user_input()
            print(result)
            print(self.menu.convert_val_to_name())
            self.assertEqual(self.menu.convert_val_to_name(), ['charge_db', 'add_entry'])
        
        # test get user db selection function with mock input
        @patch('builtins.input', side_effect=['0','0'])
        def test_user_selection_type(self, mock_input):
            user_input = self.menu.get_user_input()
            result = self.menu.user_selection_type()
            self.assertEqual(result, 'db')
        
        # test retrieval of selected db name
        @patch('builtins.input', side_effect=['0','0'])
        def test_get_selected_db_name(self, mock_input):
            user_input = self.menu.get_user_input()
            result = self.menu.get_selected_db_name()
            self.assertEqual(result.lower(), 'bike_db')

        @patch('builtins.input', side_effect=['0','0','0','0','0','0','0','0','0','0','0','0'])
        def test_user_input_add(self, mock_input):
            print("test_user_input")
            # patch different input
            user_selection = self.menu.get_entry_input('bike')
            print(user_selection)



if __name__ == '__main__':
    unittest.main()

#not working need to fix
