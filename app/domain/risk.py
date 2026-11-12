from app.domain.model import get_risk_band
from app.domain.model import predict_default_probability

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


def calculate_risk_score(customer):
    risk_score = (
        customer["credit_utilization"]*0.6
        + customer["late_payment_ratio"]*0.4
    )

    return round(risk_score,2)

def get_risk_category(risk_score):
    if risk_score >= 0.7:
        return "HIGH"
    
    if risk_score >= 0.4:
        return "MEDIUM"

    return "LOW"
