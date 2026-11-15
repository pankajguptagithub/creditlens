from app.data.payment_repository import find_payment_by_customer_id

from app.domain.model import (
        get_risk_band
        predict_default_probability
)
from app.domain.features import (
    calculate_credit_utilization,
    calculate_debt_to_income,
    calculate_late_payment_ratio
)

def calculate_risk_score(customer):
    # Simple rule-based baseline risk score
    risk_score = (
        customer["credit_utilization"]*0.6
        + customer["late_payment_ratio"]*0.4
    )

    return round(risk_score,2)

def score_customer(model, customer_features):
    # Calculate the customer's probability of default
    default_probability = predict_default_probability(
        model,
        customer_features
    )

    # Convert the probability into an understandable risk category
    risk_band = get_risk_band(default_probability)

    return{
        "default_probability": default_probability,
        "risk_band": risk_band
    }

def get_risk_category(risk_score):
    if risk_score >= 0.7:
        return "HIGH"
    
    if risk_score >= 0.4:
        return "MEDIUM"

    return "LOW"

def build_customer_features(customer,payment):
    # Build the exact feature order expected by our model
    customer_features = [
        calculate_credit_utilization(
            customer["credit_used"],
            customer["credit_limit"]
        ),
        calculate_debt_to_income(
            customer["annual_debt_obligation"],
            customer["annual_income"]
        ),
        calculate_late_payment_ratio(
            payment["late_payments"],
            payment["total_payments"]
        )
    ]
    return customer_features

def score_customer_record(model, customer, payments):
    # Find the payment history for this customer
    payment = find_payment_by_customer_id(
        payments,
        customer["customer_id"]
    )

    if payment is None:
        return None

    # Build model-ready features from customer data
    customer_features = build_customer_features(
        customer,
        payment
    )

    # Run ML-based risk scoring
    risk_result = score_customer(
        model,
        customer_features
    )

    return {
        "customer_id": customer["customer_id"],
        "default_probability": risk_result["default_probability"],
        "risk_band": risk_result["risk_band"]
    }
