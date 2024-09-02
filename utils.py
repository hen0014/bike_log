#python script containing utility functions for the project
#sub-functions for the main functions in the project
#functions to manage the database, logging, and other utilities
#Author: Henry Frankland
#Date: 04/08/2024

#imports
import bike_db
import log_config
import os
import csv
import menu
from error_handling import handle_errors

import log_config

class LogUtils:
    # setup logging
    log = log_config.LogConfig()
    logger = log.get_logger()

    @staticmethod
    @handle_errors
    def log_initialisation():
        LogUtils.logger.info("Initialisation complete")

    @staticmethod
    @handle_errors
    def log_database_connected():
        LogUtils.logger.info("Database connected")

    @staticmethod
    @handle_errors
    def log_database_disconnected():
        LogUtils.logger.info("Database disconnected")

class DatabaseUtils:
    # setup database
    db = bike_db.BikeDatabase()
    LogUtils.logger.info("Database connected")

    #get table names
    @staticmethod
    @handle_errors("Table names")
    def get_table_names():
        tables = DatabaseUtils.db.get_table_names()
        LogUtils.logger.info("Table names retrieved")
        return tables

    #get heading names for table
    @staticmethod
    @handle_errors("Table headings")
    def get_table_keys(table_name):
        keys = DatabaseUtils.db.get_table_keys(table_name)
        LogUtils.logger.info(f"Table keys retrieved for {table_name}")
        return keys

    # convert row tuple to dictionary
    @staticmethod
    @handle_errors("Convert row to dictionary")
    def row_to_dict(table_name, row):
        keys = DatabaseUtils.db.get_table_keys(table_name)
        return dict(zip(keys, row))

    #get row from table
    @staticmethod
    @handle_errors("Row retrieval")
    def get_row(table_name, id):
        #gaurd clause to check if id is a list
        if isinstance(id, list): id = id[0]
        row = DatabaseUtils.db.get_entry(table_name, id)
        LogUtils.logger.info(f"Row retrieved from {table_name}")
        return DatabaseUtils.row_to_dict(table_name, row)
    #count rows in table
    @staticmethod
    @handle_errors("Row counting")
    def count_rows(table_name):
        count = DatabaseUtils.db.count_rows(table_name)
        LogUtils.logger.info(f"Counted rows in {table_name}")
        return count

    #compare key of dictionary to table headers. return headers else return None
    @staticmethod
    @handle_errors("keys and table headings comparison")
    def key_and_table_heading_compare_dic(table_name, data):
        table_keys = DatabaseUtils.db.get_table_keys(table_name)
        return list(data.keys()) == table_keys

    #add row to table, ensure keys match table headers
    @staticmethod
    @handle_errors("Row addition")
    def add_row(table_name, data):
        if not DatabaseUtils.key_and_table_heading_compare_dic(table_name, data): return None
        new_id = DatabaseUtils.db.add_entry(table_name, data)
        LogUtils.logger.info(f"Row added to {table_name}")
        return new_id

    #delete row from table
    @staticmethod
    @handle_errors("Row deletion")
    def delete_row(table_name, id):
        DatabaseUtils.db.delete_entry(table_name, id)
        LogUtils.logger.info(f"Row deleted from {table_name}")
    
    #edit row in table
    @staticmethod
    @handle_errors("Row editing")
    def edit_row(table_name, data):
        if not DatabaseUtils.key_and_table_heading_compare_dic(table_name, data): return None
        DatabaseUtils.db.change_entry(table_name, data)
        LogUtils.logger.info(f"Row edited in {table_name}")

    #compare csv headers to table headers
    @staticmethod
    @handle_errors("keys and table headings comparison")
    def key_and_table_heading_compare_csv(table_name, import_file):
        with open(import_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            keys = next(reader)
        table_keys = DatabaseUtils.db.get_table_keys(table_name)
        return keys == table_keys 

    #csv validation
    @staticmethod
    @handle_errors("CSV validation")
    def validate_csv(import_file, table_name):
        if not os.path.exists(import_file): LogUtils.logger.error("File does not exist"); return False
        if not import_file.endswith('.csv'): LogUtils.logger.error("File is not a CSV"); return False
        if not DatabaseUtils.db.table_exists(table_name): LogUtils.logger.error("Table does not exist"); return False
        if not DatabaseUtils.key_and_table_heading_compare_csv(table_name, import_file): LogUtils.logger.error("Keys do not match table headings"); return False        
        return True

    #import csv to table
    @staticmethod
    @handle_errors("Table data import")
    def import_table(table_name, import_file):
        #gaurd clause/funtion to validate csv
        if not DatabaseUtils.validate_csv(import_file,table_name): return None
        
        #if all checks pass, import the table       
        with open(import_file, 'r') as csvfile:
            reader = csv.reader(csvfile)
            # read the first row as the keys
            keys = next(reader)
            # read the rest of the rows as the values
            values = [row for row in reader]
        DatabaseUtils.db.import_table(table_name, keys, values)
        LogUtils.logger.info("Table data imported from CSV")
    
    #import table but drop table first
    @staticmethod
    @handle_errors("Table data import after dropping table")
    def import_table_drop(table_name, import_file):
        DatabaseUtils.db.drop_table(table_name)
        DatabaseUtils.db.create_table(table_name)
        DatabaseUtils.import_table(table_name, import_file)
        LogUtils.logger.info("Table data imported from CSV after dropping table")

    #write to csv
    @staticmethod
    @handle_errors("Table data export to CSV")
    def export_table(table_name, export_file):
        data = DatabaseUtils.db.dump_table_dic(table_name)
        if data:
            with open(export_file, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(data.keys())  # Write the keys as the first row
                writer.writerows(data.values())  # Write the values as subsequent rows
            LogUtils.logger.info("Table data exported as CSV")
        else:
            LogUtils.logger.warning("No data available to export")
    
    #close connection
    @staticmethod
    @handle_errors("Database connection")
    def close_connection():
        DatabaseUtils.db.close()
        LogUtils.logger.info("Database connection closed")


    #connect to database
    @staticmethod
    @handle_errors("Database connection")
    def connect():
        DatabaseUtils.db.connect()
        LogUtils.logger.info("Database connected")

    #export table headers as csv
    @staticmethod
    @handle_errors("Table headers export to CSV")
    def export_table_headers(table_name, export_file):
        keys = DatabaseUtils.db.get_table_keys(table_name)
        with open(export_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(keys)
        LogUtils.logger.info("Table headers exported as CSV")
    
    #export all tables keys as csv
    @staticmethod
    @handle_errors("All tables headers export")
    def export_all_table_headers(dir):
        #get all table names
        tables = DatabaseUtils.get_table_names()
        #export all table headers
        for table in tables: DatabaseUtils.export_all_table_headers(table, dir+f'{table}.csv')
        LogUtils.logger.info("All table headers exported as CSV")
    
    # get all ids from a table
    @staticmethod
    @handle_errors("Get all ids")
    def get_ids(table_name):
        ids = DatabaseUtils.db.get_ids(table_name)
        LogUtils.logger.info(f"IDs retrieved from {table_name}")
        return ids

class MenuUtils:
    # setup menu
    menu = menu.user_terminal_input()

    #get menu hierarchy
    @staticmethod
    @handle_errors("Menu hierarchy")
    def get_menu_hierarchy():
        menu_hierarchy = MenuUtils.menu.get_menu_hierarchy()
        LogUtils.logger.info("Menu hierarchy retrieved")
        return menu_hierarchy

    #get user input
    @staticmethod
    @handle_errors("User input")
    def get_user_input():
        MenuUtils.menu.get_user_input()
        LogUtils.logger.info("User input retrieved")
        return MenuUtils.get_user_input_values()

    #get user input values
    @staticmethod
    @handle_errors("User input values")
    def get_user_input_values():
        values = MenuUtils.menu.user_input_values()
        LogUtils.logger.info("User input values retrieved")
        return values

    #convert value to name
    @staticmethod
    @handle_errors("Value to name conversion")
    def convert_val_to_name(menu_track, menu):
        list = []
        MenuUtils.menu.convert_val_to_name(menu_track, menu, list)
        LogUtils.logger.info("Value converted to name")
        return list
    
    #convert user input to name list
    @staticmethod
    @handle_errors("User input to name conversion")
    def convert_user_input_to_name(menu):
        values = MenuUtils.get_user_input_values()
        return MenuUtils.convert_val_to_name(values, menu)
    
    #crawl through each menu item and print like the following
    # item 1
    #  - subitem 1
    @staticmethod
    @handle_errors("Menu crawl")
    def menu_crawl():
        def crawl(menu_list, depth=0):
            for count,item in enumerate(menu_list):
                if depth >= 1 and len(menu_list) != count:
                    print("   "*depth + "├─" + item['name'])
                else:
                    print("   "*depth + "└─" + item['name'])
                if 'submenus' in item:
                    crawl(item['submenus'], depth + 1)
        crawl(MenuUtils.get_menu_hierarchy())

# quick test
if __name__ == "__main__":
    DatabaseUtils.connect()
    MenuUtils.menu_crawl()
    DatabaseUtils.close_connection()
    LogUtils.logger.info("Program complete")

    #lets get the user input
    input = MenuUtils.get_user_input()
    print(input)
    #show list as names
    print(MenuUtils.convert_user_input_to_name(MenuUtils.get_menu_hierarchy()))
    


