import psycopg2
from config import load_config

def update(contact_id):
    current_values = get_current_values(contact_id)
    if not current_values:
        print("Contact ID {contact_id} not found")
        return 0
    
    first_name = input(f'Edit the first name for contact {contact_id}: ')
    last_name = input(f'Edit the last name for contact {contact_id}: ')
    phone_number = input(f'Edit the phone number for contact {contact_id}: ')

    if first_name == "":
        first = current_values[0]
    else:
        first = first_name

    if last_name == "":
        last = current_values[1]
    else:
        last = last_name

    if phone_number == "":
        phone = current_values[2]
    else:
        phone = phone_number

    updated_row_count = 0

    sql = """UPDATE contacts
             SET first_name = %s,
                 last_name = %s,
                 phone_number = %s
             WHERE contact_id = %s"""
    try:
        config = load_config()
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                # execute the UPDATE statement
                cur.execute(sql, (first, last, phone, contact_id))
                updated_row_count = cur.rowcount
            # commit the changes to the database
            conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return updated_row_count
    
def get_current_values(contact_id):
    sql = """SELECT first_name, last_name, phone_number 
            FROM contacts 
            WHERE contact_id = %s"""
    try:
        config = load_config()
        with  psycopg2.connect(**config) as conn:
            with  conn.cursor() as cur:
                cur.execute(sql, (contact_id))
                return cur.fetchone()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

if __name__ == "__main__":
    contact_id = input("Enter the contact ID to update: ")
    update(contact_id)