def check_required_customer_fields(customer):
    # Fields required for our current feature calculations
    required_fields = [
        "customer_id",
        "annual_income",
        "annual_debt_obligation",
        "credit_limit",
        "credit_used"
    ]

    missing_fields = []

    for field in required_fields:
        if field not in customer:
            missing_fields.append(field)

    return missing_fields

def validate_customers(customers):
    # Validate every customer and collect any problems

    validation_errors = []

    for customer in customers:
        missing_fields = check_required_customer_fields(customer)

        if missing_fields:
            validation_errors.append({
                "customer_id": customer.get("customer_id"),
                "missing_fields": missing_fields
            })

            continue

        value_errors = check_customer_values(customer)

        if value_errors:
            validation_errors.append({
                "customer_id": customer.get("customer_id"),
                "value_errors": value_errors

            })

    return validation_errors

def check_required_payment_fields(payment):
    # Fields required for our current payment features

    required_fields = [
        "customer_id",
        "total_payments",
        "late_payments"
    ]

    missing_fields = []

    for field in required_fields:
        if field not in payment:
            missing_fields.append(field)

    return missing_fields

def validate_payment(payment):
    # Payment counts must exist
    if "total_payments" not in payment:
        return False

    if "late_payments" not in payment:
        return False

    # Payment counts can't be negative
    if payment["total_payments"] < 0:
        return False

    if payment["late_payments"] < 0:
        return False

    # Late payments can't exceed total payments
    if payment["late_payments"] > payment["total_payments"]:
        return False

    return True

def validate_payments(payments):
    # Validate every payment record and collect any problems
    validation_errors = []

    for payment in payments:
        missing_fields = check_required_payment_fields(payment)

        if missing_fields:
            validation_errors.append({
                "customer_id": payment.get("customer_id"),
                "missing_fields" : missing_fields

            })

            continue

        value_errors = check_payment_values(payment)

        if value_errors:
            validation_errors.append({
                "customer_id" : payment.get("customer_id"),
                "value_errors" : value_errors
            })

    return validation_errors

def check_customer_values(customer):
    # Validate basic numeric values required for feature engineering
    validation_errors = []

    if customer["annual_income"] <= 0:
        validation_errors.append("annual_income must be greather than zero")

    if customer["annual_debt_obligation"] < 0:
        validation_errors.append("annual_debt_obligation cannot be negative")

    if customer["credit_limit"] <= 0:
        validation_errors.append("credit_limit must be greather than zero")

    if customer["credit_used"] < 0:
        validation_errors.append("credit_used cannot be negative")

    return validation_errors


def check_payment_values(payment):
    # Validate payment counts before calculating payment features
    validation_errors = []

    if payment["total_payments"] <= 0:
        validation_errors.append("total_payments must be greater than zero")

    if payment["late_payments"] < 0:
        validation_errors.append("late_payments cann't be negative")

    if payment["late_payments"] > payment["total_payments"]:
        validation_errors.append(
            "late_payments cannot exceed total_payments"
        )

    return validation_errors
