from app.domain.risk import score_customer_record

from app.domain.model_evaluation import(
    calculate_evaluation_metrics,
    build_confusion_metrics
)

from app.domain.portfolio import (
    score_portfolio,
    summarize_risk_bands
)

from app.domain.model_service import (
        prepare_model_service,
        get_model_status
)        

model,customers,payments,x_test,y_test = prepare_model_service()

def verify_risk_scoring():
    # Load the three datasets used by the risk model

    risk_result = score_customer_record(
        model,
        customers[0],
        payments
    )

    print("Risk scoring:", risk_result)


verify_risk_scoring()

def display_portfolio_results():
    portfolio_results = score_portfolio(
        model,
        customers,
        payments
    )

    portfolio_summary = summarize_risk_bands(
        portfolio_results
    )

    print("Portfolio customers:",len(portfolio_results))
    print("Portfolio summary:",portfolio_summary)

display_portfolio_results()

print("Model status:", get_model_status())
