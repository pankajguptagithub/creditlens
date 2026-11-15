def explain_risk(customer_features):
    # Convert model input features into simple evidence based reasons 
    reasons = []

    credit_utilization = customer_features[0]
    debt_to_income = customer_features[1]
    late_payment_ratio = customer_features[2]

    if credit_utilization >= 0.70:
        reasons.append("High credit utilization")

    if debt_to_income >= 0.50:
        reasons.append("High debt-to-income ratio")

    if late_payment_ratio >= 0.20:
        reasons.append("Frequent late payments")

    if not reasons:
        reasons.append("No major risk factor crossed the current explanation thresholds")

    return reasons
