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
 






## Chapter 2 

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
