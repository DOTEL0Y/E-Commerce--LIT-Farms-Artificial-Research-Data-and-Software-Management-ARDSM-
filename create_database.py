#password module
import password

#Functions used to create user customer database
from generate_name import create_consumer
from generate_name import first_name
from generate_name import last_name

consumer_db = create_consumer(first_name,last_name)
# Used for pgAdmin 4 Server connect and utilize postgresql
import psycopg2
from psycopg2.extras import execute_values
#Establish connetion to Customers RSDB -> Goal to input all data from generate_name.py script into db.
try:
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password=f'{password}',
        port='5432'
    )
    with conn.cursor() as cur:
        print('connected to E-Commerce Server')
        cur.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                first_name varchar(255),
                last_name varchar(255),
                customerID int
            );
        """)
        insert_query = ("INSERT INTO customers (first_name,last_name,customerID) VALUES %s")
        execute_values(cur,insert_query,consumer_db)
        conn.commit()

except psycopg2.DatabaseError as e:
    print(f"Error connecting to Server: {e}")

except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password=f'{password}',

        port='5432'
    )
    if conn:

        with conn.cursor() as cur:
            select_customers = ('SELECT * FROM Customers;')
            cur.execute(select_customers)

            customer_records = cur.fetchall()



        print(type(customer_records),customer_records)
        x = 0
        for row in (customer_records):

            print(f"{x}:{row}")
            x +=1
        #Delete Table till script and experiment is complete. Reruns and creates table everytime it runs
        del_query = ('DROP TABLE IF EXISTS Customers;')

        cur.execute(del_query)
        conn.commit()
        print("Data Completely Deleted!")
        conn.close()
        print("Connection Closed")

#Dictionary will be used later for name_generate
customer_dict = {}

# From generate_name.py script using both variable import and function import to create customer Data.


#Data to pass is all customer information
# customer_dataset = pd.DataFrame(pass)