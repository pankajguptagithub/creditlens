import json
from deltalake import DeltaTable

def load_payments():
    # Read payment records from the local JSON file
    with open("data/payments.json","r") as file:
        payments = json.load(file)

    return payments

def find_payment_by_customer_id(payments, customer_id):
    # Finds the payment record belonging to the customer
    for payment in payments:
        if payment["customer_id"] == customer_id:
            return payment

    return None

def load_payments_from_delta():
    # Open the payment Delta table
    delta_table = DeltaTable("data/delta/payments")

    # Read the Delta table into an Arrow table
    payment_table = delta_table.to_pyarrow_table()

    # Convert the Arrow table into Python records
    payments = payment_table.to_pylist()

    return payments
