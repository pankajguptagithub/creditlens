from app.domain.risk import score_customer_record

def summarize_risk_bands(risk_results):
    # Count customers in each risk band
    summary = {
        "LOW" : 0,
        "MEDIUM" : 0,
        "HIGH" : 0
    }

    for result in risk_results:
        risk_band = result["risk_band"]
        summary[risk_band] += 1

    return summary

def calculate_average_default_probability(risk_results):
    # Calculate average probability of default across the portfolio

    if not risk_results: 
        return 0.0

    total_probability = 0.0

    for result in risk_results:
        total_probability += result["default_probability"]

    return total_probability/len(risk_results)

def find_high_risk_customers(risk_results):
    # Return only customers currently classified as high risk
    high_risk_customers = []

    for result in risk_results:
        if result["risk_band"] == "HIGH":
            high_risk_customers.append(result)

    return high_risk_customers

def score_portfolio(model,customers,payments):
    # Score every customer in the portfolio
    risk_results = []

    for customer in customers:
        risk_result = score_customer_record(
            model,
            customer,
            payments
        )

        if risk_result is not None:
            risk_results.append(risk_result)

    return risk_results
