import os
import sys
import json
import sqlite3
import pandas as pd

from Network_Security.Exception.exception import NetworkSecurityException
from Network_Security.Logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json_convertor(self, file_path):
        try:
            # Read CSV and reset index
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            # Convert DataFrame to JSON-like list of dictionaries
            records = list(json.loads(data.T.to_json()).values())
            return records
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def create_db(self, db_name):
        try:
            # Connect to SQLite database (or create it if it doesn't exist)
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()
            print(f"Database {db_name} created or connected successfully.")
            return conn, cursor
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def create_table(self, cursor, table_name, columns):
        try:
            # Create table if it doesn't already exist
            column_defs = ', '.join([f"{col} TEXT" for col in columns])
            cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs})")
            print(f"Table {table_name} created or already exists.")
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_data_sqlite(self, conn, cursor, table_name, records):
        try:
            if records:
                keys = records[0].keys()  # Get the column names from the first record
                placeholders = ', '.join(['?' for _ in keys])  # Create placeholders for each column
                columns = ', '.join(keys)  # Get the column names as a string
                values = [tuple(record.values()) for record in records]  # Prepare data for insertion
                cursor.executemany(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
                conn.commit()  # Commit changes to the database
                print(f"Inserted {len(records)} records into the table {table_name}.")
                return len(records)
            else:
                print("No records to insert.")
                return 0
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def fetch_data_from_db(self, cursor, table_name):
        try:
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            return result
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def create_json_file(self, data, file_name):
        try:
            # Create or overwrite the JSON file with the given data
            with open(file_name, 'w') as json_file:
                json.dump(data, json_file, indent=4)
            print(f"Data has been written to {file_name}")
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == '__main__':
    # Adjust file path as needed (use raw string literal or forward slashes for Windows paths)
    FILE_PATH = "DataSet/phisingData.csv"  # Update if the file is in a different location
    DATABASE = "HIMANSHU_AI.db"  # SQLite database file
    COLLECTION_NAME = "Network_Data"  # Define table name (will be used as part of JSON file name)

    networkobj = NetworkDataExtract()

    try:
        # Convert CSV data to JSON-like records
        records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
        print(records)

        # Create or connect to the SQLite database
        conn, cursor = networkobj.create_db(DATABASE)

        if records:
            # Extract column names from the first record
            columns = records[0].keys()
            # Create the table if it doesn't exist
            networkobj.create_table(cursor, COLLECTION_NAME, columns)

            # Insert records into the table
            no_of_records = networkobj.insert_data_sqlite(conn, cursor, COLLECTION_NAME, records)

            # Fetch data from the database
            data_from_db = networkobj.fetch_data_from_db(cursor, COLLECTION_NAME)

            # Create the JSON file with the database name (HIMANSHU_AI.json)
            json_file_name = f"{DATABASE.replace('.db', '')}.json"  # Creating a JSON file with the database name
            networkobj.create_json_file(data_from_db, json_file_name)

            print(f"Inserted {no_of_records} records into SQLite database {DATABASE}.")
            print(f"Data has been written to {json_file_name}.")

        else:
            print("No records to insert.")

    except NetworkSecurityException as e:
        print(f"Error: {e}")
