import pandas as pd
import seaborn as sns
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

# if input("Type y to show figure") == 'y':
#     plt.show()
