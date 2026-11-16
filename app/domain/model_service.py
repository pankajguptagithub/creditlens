from app.data.customer_repository import load_customers_from_delta
from app.data.payment_repository import load_payments_from_delta
from app.data.label_repository import load_labels_from_delta

from app.domain.training_data import build_training_data
from app.domain.model import prepare_model_data, train_model
from app.domain.risk import score_customer_record

def load_model_inputs():
    # Load all Delta datasets required for model training and scoring
    customers = load_customers_from_delta()
    payments = load_payments_from_delta()
    labels = load_labels_from_delta()

    return customers,payments,labels

def train_current_model(customers,payments,labels):
    # Build the current training dataset and train the baseline ML model
    training_data = build_training_data(
        customers,
        payments,
        labels
    )

    features, targets = prepare_model_data(training_data)
    model, x_test, y_test = train_model(
        features,
        targets
    )
    return model, x_test, y_test

def find_customer_by_id(customers,customer_id):
    # Find a customer without duplicating lookup logic in API routes
    for customer in customers:
        if customer["customer_id"] == customer_id:
            return customer
    return None

def score_customer_by_id(customer_id):
    # Orchestrate the existing Delta, model and risk-scoring layers
    customers, payments, labels = load_model_inputs()

    customer = find_customer_by_id(
        customers,
        customer_id
    )

    if customer is None:
        return None

    model, x_test, y_test = train_current_model(
        customers,
        payments,
        labels
    )

    return score_customer_record(
        model,
        customer,
        payments
    )

def prepare_model_service():
    # Prepare the common model components once
    customers, payments, labels = load_model_inputs()
    model, x_test,y_test = train_current_model(
        customers,
        payments,
        labels
    )

    return model,customers,payments,x_test,y_test
