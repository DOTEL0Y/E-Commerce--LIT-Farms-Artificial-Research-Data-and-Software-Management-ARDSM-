import pandas as pd

import traceback

import matplotlib.pyplot as plt
file = 'thc_performance.xlsx'
def read_xsls_plot(file):
    try:
        #'Unnamed: 0', 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
        dataframe = pd.read_excel(file)

        # Drop indexing column
        dataframe.drop('Unnamed: 0',axis=1,inplace=True)
        print(dataframe.columns)

        # 'product_name', 'productid','total_quantity_ordered','total_revenue'
        revenue = dataframe.drop(['thca_percentage', 'total_cbd', 'cbga', 'total_cbg','delta_nine_thc'],axis=1,inplace=False)



        fig1 =plt.figure(figsize=(10, 6))

        ax1 = fig1.add_subplot(projection='3d')

        for product in range(len(revenue['productid'])):

            ax1.plot3D((revenue['productid'][product]),[0,revenue['total_quantity_ordered'][product]],[0,revenue['total_revenue'][product]])

        # ax1.plot3D(revenue['productid'].values.tolist(),revenue['total_quantity_ordered'].values.tolist(),revenue['total_revenue'].values.tolist(),marker ='o',)
        # ax1.scatter3D(revenue['productid'].values.tolist(),revenue['total_quantity_ordered'].values.tolist(),revenue['total_revenue'].values.tolist(),cmap='viridis',marker ='o',color='red')
        ax1.set_xlabel('productid')
        ax1.set_ylabel('total_quantity_ordered')
        ax1.set_zlabel('total_revenue')


        plt.show()

    except Exception as e:
        print(f'Error output: {e}')
        traceback.print_exc()


if __name__ == '__main__':

    read_xsls_plot(file=file)


