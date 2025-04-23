import psycopg2
from config import load_config
def delete():
    sql = ""
    filter_value = ""
    map = {
    '1': 'contact_id',
    '2': 'first_name',
    '3': 'last_name',
    '4': 'phone_number'
    }
    
    
    filter = input(""" (Single choice)
                     Delete the row where:
                     1. Contact ID
                     2. First name
                     3. Last name
                     4. Phone number
                     """).strip()

    if filter != "":
        while True:
            filter_value = input("Enter the match: ")
            if filter_value != "".split():
                break

    sql += f'DELETE FROM contacts'

    if filter != "".strip():
        sql += f" WHERE {map[filter]} = '{filter_value}'"
    
    config  = load_config()
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
if __name__ == '__main__':
    delete()