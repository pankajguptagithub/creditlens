import json

def load_customers():
    # Read customer records from the local JSON file
    with open("data/customers.json","r") as file:
        customers = json.load(file)

    return customers
