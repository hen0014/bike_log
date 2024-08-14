import unittest
from unittest.mock import MagicMock
#from bike_db import BikeDB  # Assuming the class is named BikeDB


import sys
import os
# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import utils

class TestBikeDB(unittest.TestCase):

    def setUp(self):
        # Create an instance of BikeDB and mock the database connection and cursor
        self.bike_db = utils.DatabaseUtils()

        # expected table headings
        self.tables = {'bike':['id', 'entry_date', 'entry_type', 'bike_name', 'type', 'make', 'mfg_year', 'shop', 'purchase_price', 'odo', 'website_url', 'receipt_url'],
        'ebike_charge': ["id", "entry_date", "entry_type", "bike_id", "charge_date", "charge_kwh", "ppkwh", "solar_percentage", "charge_cost", "rides_per_charge"],
        'expense':["id", "entry_date", "entry_type", "bike_id", "type", "shop", "item_name", "unit_price", "quantity", "cost", "receipt_url", "website_url", "notes"],
        'maintenance':['id', 'entry_date', 'entry_type', 'bike_id', 'service_id', 'service_date', 'type', 'provider', 'work_performed', 'hours', 'cost', 'receipt_url', 'provider_url', 'notes'],
        'trips':["id", "entry_date", "entry_type", "bike_id", "ride_date", "ride_distance_kmph", "start", "destination", "strava_url"]
        }

        self.test_entry={'id': 1, 'entry_date': '2021-01-01', 'entry_type': 'test', 'bike_name': 'bike1', 'type': 'electric hybrid', 'make': 'giant', 'mfg_year': 2020, 'shop': 'bike shop', 'purchase_price': 1000, 'odo': 0, 'website_url': 'www.bike.com', 'receipt_url': 'www.receipt.com'}


    # check if bike_db is an instance of BikeDB
    def test_bike_db_instance(self):
        self.assertIsInstance(self.bike_db, utils.DatabaseUtils)
    
    # check if the tables in bike_db have the correct headings
    def test_table_headings(self):
        for table in self.tables.keys():
            self.assertEqual(self.bike_db.get_table_keys(table), self.tables[table])
    
    # insert a row into the bike table and check if the row was inserted
    def test_add_bike(self):
        id = self.bike_db.add_row("bike", self.test_entry)
        self.assertEqual(self.bike_db.get_row("bike", id), self.test_entry)
    
    #check if entry exist in table by checking a list of uuids are found
    def test_get_ids(self):
        # get a list of ids from the bike table and check if a list is returned
        self.assertTrue(isinstance(self.bike_db.get_ids("bike"), list))
    
    # list id in bike table, retreive a row and then edit the row
    def test_edit_bike(self):
        idt = self.bike_db.add_row("bike", self.test_entry)
        #get id of test entry
        #retrieve the test entry
        test_entry = self.bike_db.get_row("bike", idt[0])
        #edit the purchase price of the dictionary test_entry
        test_entry['purchase_price'] = 2000
        #edit the row in the bike table
        self.bike_db.edit_row("bike", test_entry)
        #check if the row was edited
        self.assertEqual(self.bike_db.get_row("bike", idt), test_entry)
        
if __name__ == '__main__':
    unittest.main()