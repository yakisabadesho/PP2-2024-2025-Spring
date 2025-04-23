import psycopg2
from config import load_config
def query():
    selected = []
    sql = ""
    filter_value = ""
    map = {
    '1': 'contact_id',
    '2': 'first_name',
    '3': 'last_name',
    '4': 'phone_number'
    }
    select = input(""" (To enter multiple separate choices by space)
                    Display:
                    1. Contact ID
                    2. First name
                    3. Last name
                    4. Phone number
                    (Leave empty to select all): """).split()
    filter = input(""" (Single choice)
                     Filter by:
                     1. Contact ID
                     2. First name
                     3. Last name
                     4. Phone number
                     (Leave empty to skip): """).strip()

    if filter != "":
        while True:
            filter_value = input("Enter the match: ")
            if filter_value != "".split():
                break
            
    order = input("""
                     Order by:
                     1. Contact ID
                     2. First name
                     3. Last name
                     4. Phone number
                     (Leave empty to skip): """)
    
    for choice in select:
        if choice in map:
            selected.append(map[choice])
    
    if selected == []:
        selected = ['*']
    sql += f'SELECT {', '.join(selected)}'
    sql += ' FROM contacts'

    if filter != "".strip():
        sql += f" WHERE {map[filter]} = '{filter_value}'"

    if order != "".split():
        sql += f" ORDER BY {order}"

    sql += ';'

    config  = load_config()
    print(sql)
    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                rows = cur.fetchall()
                for row in rows:
                    print(row)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
if __name__ == '__main__':
    query()