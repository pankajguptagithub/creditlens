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
    
