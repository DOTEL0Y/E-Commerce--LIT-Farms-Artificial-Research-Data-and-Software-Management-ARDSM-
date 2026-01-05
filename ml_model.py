import xgboost as xgb
import pandas as pd
import psycopg2
import traceback
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from password import password
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

def query_ascending_order():

    try:
        conn = psycopg2.connect(
            host='localhost',
            database='postgres',
            user='postgres',
            password=password,
            port='5432'
        )
        cursor = conn.cursor()

        # reorganize based on productID vs revenue value.
        ascending_order_thc_performance = ("""
        SELECT
            * 
        FROM 
            thc_performance
        
        GROUP BY
            productid
        ORDER BY
            productid ASC;""")

        cursor.execute(ascending_order_thc_performance)

        data = cursor.fetchall()


        # Return data to run on Machine Learning model.
        return data
    except Exception as e:
        print(f"Error message {e}")

    except psycopg2.DatabaseError as e:
        print(f"Error connecting to Server: {e}")
        traceback.print_exc()  # Prints the complete traceback
        print("Program continues here...")

def save_as_csv(performance_data):
    performance_data.to_csv("query_save.csv")


def xgboosting_linear(performance_data,learners):
    #Changing Configuration of XGB
    xgb.set_config(
        #Set to 2 for information
        verbosity = 2)

    x = performance_data.iloc[:,1]

    y = performance_data.iloc[:,3:10].values



    #50/50 Cross Validation 35/35
    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=.5)

    train_xgb = xgb.DMatrix(x_train,y_train,enable_categorical=True)
    test_xgb = xgb.DMatrix(x_test,y_test, enable_categorical=True)



    #Parameters for model
    params = {
        'booster':'gblinear',
        'objective':'reg:squarederror',
        'eta':.01,
        'validate_parameters': True
    }
    n = learners
    linear_model = xgb.train(params=params, dtrain=train_xgb,num_boost_round=n)

    linear_predictions = linear_model.predict(test_xgb)

    #Calculate outputs from prediction Matrix Multi-outputs
    mean_squared = mean_squared_error(y_test,linear_predictions)
    round_two = r2_score(y_test,linear_predictions)

    print(f"Mean squared Error: {mean_squared}")
    print(f"R2 Score: {round_two}")
    return mean_squared,round_two

def plot_predictions(round_two,mean_squared,number_index):

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    ax.scatter3D(round_two,mean_squared,number_index,cmap='viridis',marker ='^')

    ax.set_xlabel('X  - Round 2')
    ax.set_ylabel('Y Mean Squared')
    ax.set_zlabel('Z Learner amount')
    ax.set_title('Linear XGBoosting')

    plt.show()


def create_csv_predictions(round_two_list,mean_squared_list,number_index):

    round_two_dictionary = {
        'Learners':number_index,
        "Round Two": round_two_list
    }
    round_two_df = pd.DataFrame(round_two_dictionary).to_csv("Round2-OneTenth-50.csv")

    mean_squared_dictionary = {
        'Learners':number_index,
        'Mean Squared': mean_squared_list
    }
    mean_squared_list = pd.DataFrame(mean_squared_dictionary).to_csv("MeanSquared-OneTenth-50.csv")

if __name__ == '__main__':
    thc_overview = query_ascending_order()
    thc_overview = pd.DataFrame(thc_overview)
    round_two_list = []
    mean_squared_list = []
    number_index = []
    for learners in range(50,151):

        mean_squared, round_two = xgboosting_linear(thc_overview,learners)
        mean_squared_list.append(mean_squared)
        round_two_list.append(round_two)
        number_index.append(learners)
    create_csv_predictions(round_two_list,mean_squared_list,number_index)
    plot_predictions(round_two_list,mean_squared_list,number_index)
