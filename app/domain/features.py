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
