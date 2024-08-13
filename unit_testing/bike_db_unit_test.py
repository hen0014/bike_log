import unittest
from unittest.mock import MagicMock
from bike_db import BikeDB  # Assuming the class is named BikeDB

class TestBikeDB(unittest.TestCase):

    def setUp(self):
        # Create an instance of BikeDB and mock the database connection and cursor
        self.bike_db = BikeDB()
        self.bike_db.conn = MagicMock()
        self.bike_db.c = MagicMock()
        # expected table headings
        self.bike_db.tables = {'bike':['id', 'entry_date', 'entry_type', 'bike_name', 'type', 'make', 'mfg_year', 'shop', 'purchase_price', 'odo', 'website_url', 'receipt_url'],
        'ebike_charge': ["id", "entry_date", "entry_type", "bike_id", "charge_date", "charge_kwh", "ppkwh", "solar_percentage", "charge_cost", "rides_per_charge"],
        'expense':["id", "entry_date", "entry_type", "bike_id", "type", "shop", "item_name", "unit_price", "quantity", "cost", "receipt_url", "website_url", "notes"],
        'maintenance':["id", "entry_date", "entry_type", "bike_id", "maintenance_date", "maintenance_type", "maintenance_cost", "receipt_url", "website_url", "notes"],
        'trips':["id", "entry_date", "entry_type", "bike_id", "ride_date", "ride_distance_kmph", "start", "destination", "strava_url"]
        }
  
    #check if all table headings are present
    def tables_exist(self):
        #loop through all tables and check if they exist
        for table in self.bike_db.bike_table_headings:
            self.assertTrue(self.bike_db.table_exists(table))
    
    def bad_table_exists(self):
        #check if an error is raised if a table name that does not exist is passed
        self.assertFalse(self.bike_db.table_exists('bad_table_name'))

    def good_table_exists(self):
        #check if an error is raised if a table name that does not exist is passed
        self.assertTrue(self.bike_db.table_exists(self.bike_db.tables[0]))

    def list_instead_of_dict(self):
        #check if an error is raised if a list is passed instead of a dictionary
        self.assertFalse(self.bike_db.is_dict([1, 2, 3]))
        #check if adding a bike with a list instead of a dictionary causes a return of 1
        self.assertEqual(self.bike_db.add_bike('bike', ['Domane']), 1)

    def add_to_none_existing_table(self):
        #check if an error is raised if a table that does not exist is passed
        self.assertEqual(self.bike_db.add_bike('bad_table_name', self.bike_db.tables[self.bike.tables.keys()[0]]),1)
    
    def incorrect_table_heading(self):
        #check if an exception is thrown if a table heading that does not exist is passed
        

    

        
if __name__ == '__main__':
    unittest.main()