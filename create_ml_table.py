import pandas

import traceback

import pandas as pd
import psycopg2
from psycopg2.extras import execute_values

from password import password

try:
    conn = psycopg2.connect(
        host='localhost',
        database='postgres',
        user='postgres',
        password=password,
        port='5432'
    )
    cur = conn.cursor()

    join_thc_order_history = ("""
    SELECT 
        thc_data.product_name,
        thc_data.productid,
        thc_data.quality,
        SUM(order_history.quantity) AS total_quantity_ordered,
        SUM(order_history.total_price) as total_revenue,
        thc_data.thca_percentage,
        thc_data.total_cbd,
        thc_data.cbga,
        thc_data.total_cbg,
        thc_data.delta_nine_thc
        
    FROM 
        thc_data
    INNER JOIN 
        order_history ON TRUE
    CROSS JOIN LATERAL
        UNNEST(order_history.productid) AS order_productid(productid)
    WHERE
        thc_data.productid = order_productid.productid
    GROUP BY 
        thc_data.product_name,
        thc_data.productid;
                              """)

    cur.execute(join_thc_order_history)

    thc_performance = cur.fetchall()

    # Create XSLS from dataframe -> query list
    pd.DataFrame(thc_performance).to_excel("thc_performance.xlsx")

    cur.execute("""
        CREATE TABLE IF NOT EXISTS thc_performance(  
        product_name varchar(225),
        productid SERIAL PRIMARY KEY,
        quality char(9),
        total_quantity INT,
        total_revenue DECIMAL,
        thc_percentage DECIMAL,
        total_cbd DECIMAL,
        cbga DECIMAL,
        total_cbg DECIMAL,
        delta_nine_thc DECIMAL
        )
    """)
    performance_query = ("""
    INSERT INTO thc_performance (
        product_name,
        productid,
        quality,
        total_quantity,
        total_revenue,
        thc_percentage,
        total_cbd,
        cbga,
        total_cbg,
        delta_nine_thc) VALUES %s;
    """
    )
    execute_values(cur,performance_query,thc_performance)

    conn.commit()
    conn.close()
except psycopg2.DatabaseError as e:
    print(f"Error connecting to Server: {e}")
    traceback.print_exc()  # Prints the complete traceback
    print("Program continues here...")
except Exception as e:
    print(f"Error returned {e}")

except psycopg2.DatabaseError as e:
    print(f"Error connecting to Server: {e}")
    traceback.print_exc()  # Prints the complete traceback
    print("Program continues here...")