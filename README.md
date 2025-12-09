# E-Commerce- LIT Farms/Artificial Research Data and Software Management(ARDSM)/Tetrahydrocannabinol
<img width="440" height="400" alt="image" src="https://github.com/user-attachments/assets/fd39e44f-c01a-4396-8af5-f67d8282b774" />

pgAdmin 4/ PostgresSQL. 

<img width="200" height="400" alt="image" src="https://github.com/user-attachments/assets/e5caa501-658f-4a9b-a0e5-38829a4d2fe7" />

<img width="600" height="450" alt="image" src="https://github.com/user-attachments/assets/137cdafb-9dbb-4999-b75f-642dbe49b342" />

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

<img width="413" height="108" alt="image" src="https://github.com/user-attachments/assets/e3e3c242-295f-40fb-bacf-891e5dcf7616" />

 #### To Test this we will be using row 1
 "Patricia"	"Martin"	41343379

<img width="562" height="156" alt="image" src="https://github.com/user-attachments/assets/60080fa7-525d-4225-87b1-3dbee156edf5" />


#### Insert into table customers 
```
INSERT INTO customers ( first_name, last_name, customerid) 
VALUES ( 'Oscary', 'Dotel', 41343379);
```
Note the customerID from 

'Patricia' and 'Oscary' are both 41343379.


Run all the code from above to verify that there are duplicate customerIDs 











#### After running, query: Query to check if any duplicates CustomerIDs
SELECT *
FROM Customers 
WHERE customerid IN (
SELECT customerid FROM Customers Group by customerid
HAVING COUNT(*) > 1
);

Now, I will run the query to delete these additional rows.

# Query to delete if any duplicates CustomerIDs

DELETE FROM Customers 
WHERE customerid IN ( 
	SELECT customerid 
	FROM Customers 
	Group by customerid 
	HAVING COUNT(*) > 1 
);








I will now insert:
 # "Patricia"	"Martin"	41343379 

back into the customers table.

# Insert into table customers 

INSERT INTO customers ( first_name, last_name, customerid) 
VALUES ( "Patricia",	"Martin",41343379 );








## Chapter 2 

Inserting Product information,

Inserting Chemical data 


Tables → Columns for Products 
#### 'ProductID' int, 'Name' varchar(255), 'Strain' varchar(255), 'Price ' int, 'Size ' char, 'Nug'   # char, 'Quality 'char, 'Total CBD',

CREATE TABLE IF NOT EXISTS products (  
	productid int, 
	product_name varchar(255), 
	Strain char(16),
	price float,
	size_g int,
	nug char(7),
	quality char(4),
	total_cbd float
);

This is the query to create the product table if it does not exists

Now we will make the chemical data table and call it thc_data
With columns:
#### 'ProductID' int, 'Name' varchar(255), 'Strain' varchar(255),  'Nug' char, 'Quality 'char,
#### 'THCa%', 'Total CBD', 'CBGA', 'Total CBG', 'Δ9-THC'
```
CREATE TABLE IF NOT EXISTS thc_data (
	productid int, 
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



