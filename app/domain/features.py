from app.data.payment_repository import find_payment_by_customer_id

def calculate_credit_utilization(credit_used, credit_limit):
    # Calculate how much of the available credit is being used
    utilization = credit_used / credit_limit

    return utilization

def add_credit_utilization(customer):
    # Calculate utilization using the customer's credit values
    utilization = calculate_credit_utilization(
        customer["credit_used"],
        customer["credit_limit"]
    )
    customer["credit_utilization"] = utilization
    return customer

def calculate_late_payment_ratio(late_payments, total_payments):
    # Calculate the proportion of payments that were late
    late_payment_ratio = late_payments / total_payments
    return late_payment_ratio

def add_payment_features(customer, payment):
    # Add raw payment information to the customer
    customer["total_payemnts"] = payment["total_payments"]
    customer["late_payments"] = payment["late_payments"]

    # Calcuate the customer's late payment ratio
    customer["late_payment_ratio"] = calculate_late_payment_ratio(
        payment["late_payments"],
        payment["total_payments"]
    )
    return customer

def add_payment_features_to_customers(customers,payments):
    # Add payment features to every customer
    for customer in customers:
        customer_id = customer["customer_id"]

        payment = find_payment_by_customer_id(
            payments,
            customer_id
        )

        if payment is not None:
            add_payment_features(customer,payment)

    return customers

def calculate_debt_to_income(annual_debt_obligation, annual_income):
    # Calculate how much of annual income goes toward debt obligations
    debt_to_income = annual_debt_obligation / annual_income

    return debt_to_income

def add_debt_to_income(customer):
    # Calculate the customer's debt-to-income ratio
    debt_to_income = calculate_debt_to_income(
        customer["annual_debt_obligation"],
        customer["annual_income"]
    )

    customer["debt_to_income"] = debt_to_income
    
    return customer
