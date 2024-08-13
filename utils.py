#python script containing utility functions for the project
#sub-functions for the main functions in the project
#functions to manage the database, logging, and other utilities
#Author: Henry Frankland
#Date: 04/08/2024

#imports
import bike_db.py
import log_config.py
import os
import csv
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
        return data.keys() == table_keys

    #add row to table, ensure keys match table headers
    @staticmethod
    @handle_errors("Row addition")
    def add_row(table_name, data):
        if not DatabaseUtils.key_and_table_heading_compare_dic(table_name, data): return None
        DatabaseUtils.db.add_entry(table_name, data)
        LogUtils.logger.info(f"Row added to {table_name}")

    #delete row from table
    @staticmethod
    @handle_errors("Row deletion")
    def delete_row(table_name, id):
        DatabaseUtils.db.delete_entry(table_name, id)
        LogUtils.logger.info(f"Row deleted from {table_name}")
    
    #edit row in table
    @staticmethod
    @handle_errors("Row editing")
    def edit_row(table_name, id, data):
        if not DatabaseUtils.key_and_table_heading_compare_dic(table_name, data): return None
        DatabaseUtils.db.edit_row(table_name, id, data)
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