<img width="300" height="300" alt="image" src="https://github.com/user-attachments/assets/348aaae0-8d6d-4b2d-ab04-d0324ba69e29" />
<img width="350" height="300" alt="image" src="https://github.com/user-attachments/assets/bb6f1189-14d6-4c3c-bdfa-552179fd7d0b" />



# E-Commerce--LIT-Farms-Artificial-Research-Data-and-Software-Management-ARDSM-Tetrahydrocannabinol



## Installation 

As an important note. I utilized python 3.1 intrepreter to avoid conflicts with dependies 
```
pip install openpyxl
pip install pandas
pip install psycopg2-binary
pip install matplotlib


```

## Chapter 1: Create Artificial Customers
 
The first step was to design a script that would create a customer list for me to work with. 


#### Python Module: random

With this module I was able to create a list of customers with a unique 8 digit customerID.
```
import random

first_name = ["James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda",
    "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph",
    "Jessica", "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy",
    "Daniel", "Lisa", "Matthew", "Betty", "Anthony", "Helen", "Mark", "Sandra",
    "Donald", "Donna", "Steven", "Carol", "Paul", "Ruth", "Andrew", "Sharon",
    "Kenneth", "Michelle"]


last_name = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Thomas", "Taylor", "Moore", "Jackson", "White", "Harris", "Martin", "Thompson",
    "Garcia", "Martinez", "Robinson", "Wright", "Flores", "Torres", "Nguyen",
    "Hill", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Parker",
    "Evans", "Edwards"]


# Function used to send out init/Main script
# Return list Tuple -> Last_name, First_name, CustomerID
def create_consumer(first_name,last_name):

    consumer_amount = 0

    consumer_list = []

    min_value = 10000000
    max_value = 99999999

    for x in range(400):

        random_first_name = random.choice(first_name)

        random_last_name = random.choice(last_name)

        customer_id = random.randint(min_value, max_value)

        consumer_list.append((random_first_name,random_last_name,customer_id))

    return consumer_list







```


 #### Query to check if any duplicates CustomerIDs

```
SELECT *
FROM Customers 
WHERE customerid IN (
SELECT customerid FROM Customers Group by customerid
HAVING COUNT(*) > 1
);
```

#### Query to delete any duplicates within Python script.

        #Delete Table till script and experiment is complete. Reruns and creates table everytime it runs
        del_query = ('DROP TABLE IF EXISTS Customers;')
        cur.execute(del_query)
        # make sure to commit changes
        conn.commit()

#### Query to delete if any duplicates CustomerIDs in Pgadmin4
```
DELETE FROM Customers 
WHERE customerid IN ( 
	SELECT customerid 
	FROM Customers 
	Group by customerid 
	HAVING COUNT(*) > 1 
);
```
 #### To Test this we will be using row 1
 "Patricia"	"Martin"	41343379

    ### Insert Image here
<img width="684" height="97" alt="image" src="https://github.com/user-attachments/assets/2df2ca2d-ca0b-4181-b48e-3e3264379960" />

```
INSERT INTO customers ( first_name, last_name, customerid) 
VALUES ( 'Oscary', 'Dotel', 41343379);
```
Note the customerID from 

'Patricia' and 'Oscary' are both 41343379.


Run all the code from above to verify that there are duplicate customerIDs 


<img width="675" height="136" alt="image" src="https://github.com/user-attachments/assets/fd0d6ab9-ea91-4e0f-a127-c008ff0f1dd6" />








#### After running, query: Query to check if any duplicates CustomerIDs
SELECT *
FROM Customers 
WHERE customerid IN (
SELECT customerid FROM Customers Group by customerid
HAVING COUNT(*) > 1
);

Now, I will run the query to delete these additional rows.

### Query to delete if any duplicates CustomerIDs
```
DELETE FROM Customers 
WHERE customerid IN ( 
	SELECT customerid 
	FROM Customers 
	Group by customerid 
	HAVING COUNT(*) > 1 
);
```

<img width="413" height="108" alt="image" src="https://github.com/user-attachments/assets/38da2e20-22a1-4f2e-beab-8ac2cc5665d9" />






I will now insert:
 #### "Patricia"	"Martin"	41343379 

back into the customer's table.




#### Insert into table customers 
```
INSERT INTO customers ( first_name, last_name, customerid) 
VALUES ( "Patricia",	"Martin",41343379 );
```

<img width="388" height="90" alt="image" src="https://github.com/user-attachments/assets/207785b6-a7fa-46d5-8afd-763550fd40dd" />
 






## Chapter 2: Create and insert LIT Farms DATA

In this chapter, we will cover inserting the XLSX from the LIT Farms product list. 
It will include splicing the data into multiple dataframes to then upload to a database as a table.

Please View -> Tetrahydra-canabinol.xslx

```
import pandas as pd
import matplotlib

from password import password as pwd
password = pwd

# Used for pgAdmin 4 Server connect and utilize postgresql
import psycopg2
from psycopg2.extras import execute_values

file_name = 'Tetrahydra-canabinol .xlsx'

# 'ProductID', 'Name', 'Strain', 'Price ', 'Size ', 'Nug', 'Quality ',
# 'THCa%', 'Total CBD', 'CBGA', 'Total CBG', 'Δ9-THC'
def create_dataframe(file):

    # Opens xlsx as dataframe
    dataframe = pd.read_excel(file_name)

    # Drops Source column, won't be necessary for database
    dataframe.drop(columns='source',inplace=True)

    # Dataframe for chemical data -> Price and Size is related to purchase
    chemical_columns_drop = ['Price ', 'Size ',]
    # Create DF from original df without price and size
    chemical_data_frame = dataframe.drop(columns = chemical_columns_drop,inplace=False)
    chemical_data_frame.to_excel('chemical_data.xlsx', index=False, sheet_name='chemical')



    # Commerce Dataframe wont need chemical data as it is not necessary for purchases other than total CBD as it can be used as a label for customer reference
    commerce_columns_drop = ['THCa%', 'CBGA', 'Total CBG', 'Δ9-THC']

    # Dataframe for E-Commerce
    commerce_dataframe = dataframe.drop(columns = commerce_columns_drop,inplace=False)
    commerce_dataframe.to_excel('commerce_data.xlsx', index=False, sheet_name='commerce')


    return commerce_dataframe,chemical_data_frame,dataframe

def plot_data():
    commcerce, chemical, dataframe = create_dataframe(file_name)

    # 'THCa%', 'Total CBD', 'CBGA', 'Total CBG', 'Δ9-THC'
    # There are the columns that we will turn into a list for the sake of plotting
    # Using .tolist()
    name = chemical['Name'].to_numpy().tolist()
    total_cbd = chemical['Total CBD'].to_numpy().tolist()
    thca_percentage = chemical['THCa%'].values.tolist()
    cbga = chemical['CBGA'].values.tolist()
    total_cbg = chemical['Total CBG'].values.tolist()

    delta_9 = chemical['Δ9-THC'].values.tolist()

    import matplotlib.pyplot as plt

    # Import the mplot3d toolkit (necessary for 3d axes setup)
    from mpl_toolkits.mplot3d import Axes3D
    fig1 =plt.figure(figsize=(10, 6))

    ax1 = fig1.add_subplot(projection='3d')


    # ax1.scatter3D(thca_percentage, total_cbd, total_cbg,s=delta_9, c=  cbga,cmap='viridis', marker ='^')
    ax1.scatter3D(thca_percentage,total_cbd,total_cbg,cmap='viridis',marker ='^')
    ax1.set_xlabel('Total CBD')
    ax1.set_ylabel("Total CBG")
    ax1.set_zlabel("THCa %")

    if input("Type y to show figure") == 'y':
        plt.show()


if __name__ == '__main__':
    plot_data()

```

### Figure 1:Plot Chart [X: Total CBD, Y:THCa%, Z: Total CBG]


<img width="898" height="677" alt="image" src="https://github.com/user-attachments/assets/85a0abba-1e89-461f-9278-bd07e1838d0f" />
This chart was created by matplotlibs. Showing the ranges of chemical data present.  I will use this chart for reference when introducing new product to virtual market to simulate consumerism response to new product. The ideal here is to understand how this chart and the plots influence buying trends. A model that can predict based on trends and consumer trajectory. 


#### Tables → Columns for Products  
#### 'ProductID', 'product_name', 'Strain', 'Price ', 'Size ', 'Nug', 'Quality ', 'Total CBD',


<img width="659" height="306" alt="image" src="https://github.com/user-attachments/assets/dd3496df-7705-4c51-a43e-e8ee01e43998" />

##### This is the query to create the product table if it does not exist
```
CREATE TABLE IF NOT EXISTS products (  
	productid SERIAL PRIMARY KEY, 
	product_name varchar(255), 
	Strain char(16),
	price float,
	size_g int,
	nug char(7),
	quality char(4),
	total_cbd float
);
commerce_query = ('INSERT INTO products (productid, product_name , Strain ,price ,size_g ,nug ,quality,total_cbd) VALUES %s')
execute_values(cur,commerce_query,commerce_data.values.tolist())
```


Now we will make the chemical data table and call it thc_data
With columns:
#### Tables → Columns for THC_data
#### 'ProductID', 'product_name', 'Strain',  'Nug', 'Quality ',
#### 'THCa%', 'Total CBD', 'CBGA', 'Total CBG', 'Δ9-THC'
```
CREATE TABLE IF NOT EXISTS thc_data (
	productid SERIAL PRIMARY KEY, 
	product_name varchar(255), 
	strain char(16),
	nug char(6),
	quality char(4),
	thca_percentage float,
	total_cbd float,
	cbga  float,
	total_cbg float,
	delta_nine_thc float
);

```

#### Python Example commerce:
```
cur.execute("""
    CREATE TABLE IF NOT EXISTS products (  
        productid int, 
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
commerce_query = ('INSERT INTO products (productid, product_name , Strain ,price ,size_g ,nug ,quality,total_cbd) VALUES %s')
execute_values(cur,commerce_query,commerce_data.values.tolist())
```








<img width="1237" height="213" alt="image" src="https://github.com/user-attachments/assets/ad8763e7-845b-435a-926d-894872db63d2" />


#### Python Example Chemical data:
```
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

chemical_query = ('INSERT INTO thc_data (productid, product_name , Strain ,nug ,quality,thca_percentage,total_cbd,cbga,total_cbg,delta_nine_thc) VALUES %s')
execute_values(cur,chemical_query,chemical_data.values.tolist())
````
<img width="1550" height="300" alt="image" src="https://github.com/user-attachments/assets/a4cda697-3e0c-49e9-aba4-875251c0c524" />


## Chapter 3: Create artificial Orders and OrderHistory data

The goal of this is now to take the query the customerID and with that data construct artificial orders from 2024, Dec -> 2025, Dec

### Chapter 3.1: Generate orders script!~
Below is the code. 
Note that I imported pandas to achieve this as well.

```
import pandas as pd
import psycopg2
import pandas
from password import password

import random
from datetime import date,timedelta




# Random Date function

def random_date_no_time(start_date,end_date):

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
        print(customerID_data)
        for id in customerID_data['customerID']:


            number_of_orders = random.randint(1,5)

            for order in range(number_of_orders):
                random_date = random_date_no_time(start_date,end_date)
                random_orderid = random.randint(min_value,max_value)

                create_order = (random_orderid, id,random_date)
                orders.append(create_order)

        # orders = pd.DataFrame(orders,columns=['OrderID','CustomerID','Date'])
        print(orders)
        conn.commit()
        conn.close()
    except psycopg2.DatabaseError as e:
        print(f"Error {e}")
    return orders

if __name__ == '__main__':

    generate_customer_orders()

```

Now to add this data to the generate_database.py script. 

```
    # Create Orders table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders(
        orderid SERIAL PRIMARY KEY,
        customerid int,
        date date
        )
    """)

    orders_query = ('INSERT INTO orders (orderid,customerid,date) VALUES %s')
    execute_values(cur,orders_query,generate_customer_orders())
```


Now to query this in pgadmin4 to see if it was constructed correctly

```
SELECT * FROM orders;
```
Yes, just the way we want it!

<img width="389" height="222" alt="image" src="https://github.com/user-attachments/assets/2e6ddc0c-66ce-47bd-a6d5-15773f665993" />


### Chapter 3.2: Generate OrderHistory!~


To achieve this, I will also use similar techniques and methods shown previously.
Mathematically, this a very important part of the scripting and generation of artificial data because the columns/rows generated here will dictate how our Machine learning model responses to the consumer purchases in relation to the chemical data. In a real scenario Data engineering and filtering among ideal HISTORICAL data is crucial due to 1. Gathering of data that is most relevant to the current scenario or problem 2. If big data is available to avoid over training the model.
In those circumstances, cross-validation would need to be experimented on through responsive neural networks of historical data and present/incoming data to predict trends.
Here is the script I made to generate described data

```
import pandas as pd
import psycopg2
import pandas

import random
from password import password


def create_order_history():
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password=password,
        port='5432'
    )

    cur = conn.cursor()

    gather_orders_query = 'SELECT * FROM orders'

    cur.execute(gather_orders_query)

    orders_data = cur.fetchall()

    gather_product_query = 'SELECT * FROM Products'

    cur.execute(gather_product_query)

    product_data = cur.fetchall()



    order_history = []
    for index,order in enumerate(orders_data):
        product_purchased = []
        price = 0.00
        # 10 randomly purchased products that will be used in forloop
        random_amount_purchase = random.randint(1,10)
        order_index = index
        order_id = order[0]
        # print(order_id,order)
        for purchase_index in range(random_amount_purchase):
            random_product = random.choice(product_data)
            product_purchased.append([random_product[0]])
            price += random_product[3]
        order_history.append([order_id,product_purchased,f"${round(price, 2)}"])
    # pd.DataFrame(order_history).to_csv('output_example.csv')
    return(pd.DataFrame(order_history))


if __name__ == '__main__':
    data = create_order_history()

    data = pd.DataFrame(data, columns=['orderid','customereid','date'])

    # print(data)


```

### Now to import this into the database for later use! (back to create_database.py)

```

    # Create OrderHistory table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_History(
        detailsid int PRIMARY KEY,
        orderid int,
        productid int[],
        quantity int,
        total_price decimal
        )
    """)
    
    order_details_query = 'INSERT INTO order_History (DetailsID,orderid,productid,quantity,total_price) VALUES %s'
    execute_values(cur,order_details_query,generate_order_history())
```
<img width="795" height="175" alt="image" src="https://github.com/user-attachments/assets/78a38c5e-b696-48dc-9f04-bf7a2018c26f" />

Similar code to previous table creations. 
Only difference in this query is productid. Considering it is an array of products that the costumer purchased – bracket notation is required to INSERT the data correctly.

 


