#password module
from password import password as pwd

import traceback

#Functions used to create user customer database
from generate_name import create_consumer
from generate_name import first_name
from generate_name import last_name

# Obtain function from create consumer
consumer_db = create_consumer(first_name,last_name)

# Used for pgAdmin 4 Server connect and utilize postgresql
import psycopg2
from psycopg2.extras import execute_values

# From splice_xlsx.py obtaining dataframe to upload productList to
from splice_xlsx import create_dataframe as xlsx
from splice_xlsx import file_name

commerce_data, chemical_data,raw_data = xlsx(file_name)

print(type(chemical_data),chemical_data)

#Establish connetion to Customers RSDB -> Goal to input all data from generate_name.py script into db.
password = pwd

try:
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password=password,
        port='5432'
    )
    cur = conn.cursor()
    print('connected to E-Commerce Server')

    # Creates customers table IF it doesn't exists
    # 'first_name' varchar(255), 'last_name' varchar(255), customerid int
    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            first_name varchar(255),
            last_name varchar(255),
            customerID SERIAL PRIMARY KEY
        );
    """)

    ## Used for inserting customers from generate_name.py script with total of 50 customers
    # insert_query_customers = ("INSERT ON CONFLICT DO NOTHING INTO customers (first_name,last_name,customerID) VALUES %s")
    # execute_values(cur,insert_query_customers,consumer_db)

    # Deletes duplicate customers found from query
    insert_query = ('DELETE FROM Customers WHERE customerid IN ( SELECT customerid FROM Customers Group by customerid HAVING COUNT(*) > 1 );')

    ## Creates Product DATABASE
    ## 'ProductID', 'Name', 'Strain', 'Price', 'Size', 'Nug', 'Quality',
    ## 'Total CBD'
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (  
            productid SERIAL PRIMARY KEY, 
            product_name varchar(255), 
            Strain char(16),
            price float,
            size_g int,
            nug char(7),
            quality char(9),
            total_cbd float
        );
    """
     )
    # commerce_query = ('INSERT INTO ON CONFLICT DO NOTHING products (productid, product_name , Strain ,price ,size_g ,nug ,quality,total_cbd) VALUES %s')
    # execute_values(cur,commerce_query,commerce_data.values.tolist())


    # Create THC DATABASE
    ## 'ProductID', 'Name', 'Strain' , 'Nug' char, 'Quality',
    ## 'THCa%', 'Total CBD', 'CBGA', 'Total CBG', 'Δ9-THC'
    cur.execute("""
        CREATE TABLE IF NOT EXISTS thc_data (
            productid SERIAL PRIMARY KEY, 
            product_name varchar(255), 
            strain char(16),
            nug char(9),
            quality char(9),
            thca_percentage float,
            total_cbd float,
            cbga  float,
            total_cbg float,
            delta_nine_thc float
        );
    """)

    # chemical_query = ('INSERT INTO thc_data (productid, product_name , Strain ,nug ,quality,thca_percentage,total_cbd,cbga,total_cbg,delta_nine_thc) VALUES %s')
    # execute_values(cur,chemical_query,chemical_data.values.tolist())





    select_products = ('SELECT * FROM Products;')
    cur.execute(select_products)
    all_products = cur.fetchall()

    select_chemical = ('SELECT * FROM thc_data')
    cur.execute(select_chemical)
    all_chemical = cur.fetchall()

    print("Code Commited",all_products,all_chemical)
    conn.commit()

except psycopg2.DatabaseError as e:
    print(f"Error connecting to Server: {e}")
    traceback.print_exc()  # Prints the complete traceback
    print("Program continues here...")

except Exception as e:
    print(f"An unexpected error occurred: {e}")

finally:
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password=password,
        port='5432'
    )
    if conn:
            cur2 = conn.cursor()

            select_customers = ('SELECT * FROM Customers;')
            cur2.execute(select_customers)

            customer_records = cur2.fetchall()





    print(type(customer_records),customer_records)

        #Delete Table till script and experiment is complete. Reruns and creates table everytime it runs
        # del_query = ('DROP TABLE IF EXISTS Customers;')
        #
        # cur.execute(del_query)
        # conn.commit()
        # print("Data Completely Deleted!")
    cur2.close()
    conn.close()
    print("Connection Closed")

#Dictionary will be used later for name_generate
customer_dict = {}

# From generate_name.py script using both variable import and function import to create customer Data.


#Data to pass is all customer information
# customer_dataset = pd.DataFrame(pass)