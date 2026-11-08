import json
from deltalake import DeltaTable

def load_customers():
    # Read customer records from the local JSON file
    with open("data/customers.json","r") as file:
        customers = json.load(file)

    return customers

def load_customers_from_delta():
    # Open the customer delta table 
    delta_table = DeltaTable("data/delta/customers")

    # Read the Delta table into an Arrow table
    customer_table = delta_table.to_pyarrow_table()

    # Convert the Arrow table into Python records
    customers = customer_table.to_pylist()

    return customers
