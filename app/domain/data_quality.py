def validate_customer_id(customer):
    # check that every customer has an identifier 

    if "customer_id" not in customer:
        return False

    return True

def validate_annual_income(customer):
    # Annual income must exist and must be greater than zero

    if "annual_income" not in customer:
        return False

    if customer["annual_income"] <= 0:
        return False

    return True

def validate_customer(customer):
    # A customer is valid only when all customer checks pass
    if not validate_customer_id(customer):
        return False

    if not validate_annual_income(customer):
        return False

    return True

def validate_customers(customers):
    # Collect customer IDs that fail validation
    invalid_customers = []

    for customer in customers:
        if not validate_customer(customer):
            invalid_customers.append(customer["customer_id"])

    return invalid_customers
