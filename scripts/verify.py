from app.data.customer_repository import load_customers_from_delta
from app.data.payment_repository import load_payments_from_delta
from app.data.label_repository import load_labels_from_delta

from app.domain.training_data import build_training_data
from app.domain.model import prepare_model_data, train_model
from app.domain.risk import score_customer_record


def verify_risk_scoring():
    # Load the three datasets used by the risk model
    customers = load_customers_from_delta()
    payments = load_payments_from_delta()
    labels = load_labels_from_delta()

    # Build model-ready training data
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

    # Verify scoring against one real Delta customer
    risk_result = score_customer_record(
        model,
        customers[0],
        payments
    )

    print("Risk scoring:", risk_result)


verify_risk_scoring()
