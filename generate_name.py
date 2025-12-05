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
    if len(last_name) > len(first_name):
        consumer_amount = len(last_name)
    else:
        consumer_amount = len(first_name)

    for x in range(consumer_amount):

        random_first_name = random.choice(first_name)

        random_last_name = random.choice(last_name)

        customer_id = random.randint(min_value, max_value)

        consumer_list.append((random_first_name,random_last_name,customer_id))

    return consumer_list






