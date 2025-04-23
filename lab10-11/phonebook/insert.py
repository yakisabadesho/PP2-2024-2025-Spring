import psycopg2
import csv
import os
from config import load_config

def insert_name(first_name, last_name, phone_number):
    sql = """INSERT INTO contacts(first_name, last_name, phone_number)
             VALUES(%s, %s, %s) RETURNING contact_id;"""
    contact_id = None
    config = load_config()
    try:
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the INSERT statement
                cur.execute(sql, (first_name, last_name, phone_number))
                # get the generated id back
                rows = cur.fetchone()
                if rows:
                    contact_id = rows[0]
                # commit the changes to the database
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return contact_id
    
def csv_insert(path):
    inserted_count = 0
    try:
        with open(path, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                if len(row) == 3:
                    contact_id = insert_name(row[0], row[1], row[2])
                if contact_id:
                    inserted_count += 1
        if contact_id:
            print(f"{inserted_count} users inserted successfully from {path}.")
        else:
            print("No valid data found in the CSV file.")
    except FileNotFoundError:
        print(f"File not found: {path}")
    except Exception as error:
        print(f"Error reading CSV file: {error}")

if __name__ == '__main__':
    while True:
        choice = int(input("""Choose insertion method:
            1. Manual
            2. From .csv file
            """))
        if choice != 1 and choice != 2:
            print("Please enter either 1 or 2")
        else:
            break
    if choice == 1:
        first_name = input("Enter the first name: ")
        last_name = input("Enter the last name: ")
        while True:
            try:
                phone_number = int(input("Enter the phone number: "))
            except:
                print("Please input a number")
            else:
                break
        insert_name(first_name, last_name, phone_number)
    if choice == 2:
        path = input("Please enter the path: ")
        csv_insert(path)