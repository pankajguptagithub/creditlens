import json

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
