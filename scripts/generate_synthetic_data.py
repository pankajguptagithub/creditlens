import random
import pyarrow as pa

from app.core.config import load_config
from deltalake import write_deltalake

def generate_customers():
    config = load_config()

    customer_count = config["synthetic_customer_count"]
    random_seed = config["synthetic_random_seed"]

    # Fixed seed makes our generated data reproducable
    random.seed(random_seed)

    customers = []

    for number in range(1, customer_count + 1):
        annual_income = random.randint(400000,2000000)
        credit_limit = random.randint(100000,600000)
        credit_used = random.randint(0, credit_limit)

        customer = {
            "customer_id": f"C{number:03d}",
            "annual_income": annual_income,
            "annual_debt_obligation": random.randint(
                50000,
                annual_income
            ),
            "credit_limit": credit_limit,
            "credit_used": credit_used
        }

        customers.append(customer)

    return customers

def generate_payments(customers):
    # Generate payment behavior for every synthetic customer
    payments = []

    for customer in customers:
        total_payments = 12
        late_payments = random.randint(0,6)

        payment = {
            "customer_id": customer["customer_id"],
            "total_payments": total_payments,
            "late_payments" : late_payments
        }

        payments.append(payment)

    return payments

def generate_labels(customers,payments):
    # Generate synthetic historical dfault outcomes
    labels = []

    for customer,payment in zip(customers,payments):
        credit_utilization = (
            customer["credit_used"] / customer["credit_limit"]
        )

        debt_to_income = (
            customer["annual_debt_obligation"]/customer["annual_income"]
        )

        late_payment_ratio = (
            payment["late_payments"]
            / payment["total_payments"]
        )

        # High-risk behavior increases the chance of synthetic default
        default_probability = (
            0.05
            + (0.30 * credit_utilization)
            + (0.25 * debt_to_income)
            + (0.40 * late_payment_ratio)
        )

        default_probability = min(default_probability, 0.95)
        defaulted = 1 if random.random() < default_probability else 0

        labels.append({
            "customer_id": customer["customer_id"],
            "defaulted": defaulted
        })

    return labels

def write_to_delta(data, delta_path):
    # Convert Python records into an Arrow table
    table = pa.Table.from_pylist(data)

    # Store the generated dataset as a Delta table
    write_deltalake(
        delta_path,
        table,
        mode = "overwrite",
    )

def generate_all_data():
    customers = generate_customers()
    payments = generate_payments(customers)
    labels = generate_labels(customers, payments)

    write_to_delta(
        customers,
        "data/delta/customers"
    )

    write_to_delta(
        payments,
        "data/delta/payments"
    )

    write_to_delta(
        labels,
        "data/delta/labels"
    )

generate_all_data()
