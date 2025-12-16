import pandas as pd
import psycopg2
import pandas
from password import password

import random
from datetime import date,timedelta




# Random Date function

def random_date_no_time(start_date,end_date):

    """
    :param start_date: datatype Date - beginning days
    :param end_date:  datatyep Date - ending days
    :return: random date from 2024-2025
    """

    dif_days = (end_date-start_date).days

    random_day = random.randint(0,dif_days)

    random_date = start_date + timedelta(days =random_day)

    return random_date
from psycopg2.extras import  execute_values
def generate_customer_orders():

    orders = []
    try:

        # Establish connection to database
        conn = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='postgres',
            password=password,
            port='5432'
        )
        # Create cursor variable to execute
        cur = conn.cursor()

        # Obtain data query from Customers
        gather_customer_data = 'SELECT * FROM customers'
        cur.execute(gather_customer_data)

        # Obtained data in list format
        data_customers = cur.fetchall()

        # list -> to df for column drops
        customer_data = pd.DataFrame(data_customers, columns=['first_name','last_name','customerID'])

        # Dropping columns first_name, last_name
        customerID_data = customer_data.iloc[:,[2]]


        # Obtain data of products query
        gather_products_data = 'SELECT productID FROM Products'
        cur.execute(gather_products_data)
        products_data = cur.fetchall()
        products_data = pd.DataFrame(products_data,)



        # Datetime parameters for 1 year
        start_date = date(2024, 12,31)
        end_date = date(2025,12,31)


        # Int var for random orderID
        min_value = 10000000
        max_value = 99999999

        for id in customerID_data['customerID']:


            number_of_orders = random.randint(1,5)



            for order in range(number_of_orders):
                random_date = random_date_no_time(start_date, end_date)
                random_orderid = random.randint(min_value, max_value)
                create_order = (random_orderid, id,random_date)
                orders.append(create_order)

        # orders = pd.DataFrame(orders,columns=['OrderID','CustomerID','Date'])
        print(orders)
        conn.commit()
        conn.close()
        print("generate_orders.py. commited and closed!")
    except psycopg2.DatabaseError as e:
        print(f"Error {e}")
    return orders

if __name__ == '__main__':

    generate_customer_orders()
