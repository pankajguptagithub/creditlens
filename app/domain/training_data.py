from app.domain.features import (
    calculate_credit_utilization,
    calculate_debt_to_income,
    calculate_late_payment_ratio
    
)
from app.data.payment_repository import find_payment_by_customer_id

def find_label_by_customer_id(labels,customer_id):
    # Find the historical default label for a customer

    for label in labels:
        if label["customer_id"] == customer_id:
            return label

    return None

def build_training_record(customer,payment,label):
    # Build the features that our future model will learn from 

    training_record = {
        "customer_id": customer["customer_id"],
        "credit_utilization": calculate_credit_utilization(
            customer["credit_used"],
            customer["credit_limit"]
        ),
        "debt_to_income": calculate_debt_to_income(
            customer["annual_debt_obligation"],
            customer["annual_income"]
        ),
        "late_payment_ratio": calculate_late_payment_ratio(
            payment["late_payments"],
            payment["total_payments"]
        ),
        "defaulted": label["defaulted"]
    }

    return training_record

def build_training_data(customers,payments,labels):
    # Build one model-training record for each customer 
    training_data = []

    for customer in customers:
        customer_id = customer["customer_id"]

        payment = find_payment_by_customer_id(
            payments,
            customer_id
        )

        label = find_label_by_customer_id(
            labels,
            customer_id
        )

        if payment is not None and label is not None:
            training_record = build_training_record(
                customer,
                payment,
                label
            )
            training_data.append(training_record)

    return training_data
