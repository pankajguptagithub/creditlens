import logging
import re

from fastapi import FastAPI, HTTPException
from app.core.config import load_config
from app.core.logging_config import setup_logging
from app.domain.features import (
        add_credit_utilization,
        add_debt_to_income,
        add_payment_features_to_customers
)
from app.domain.risk import calculate_risk_score, get_risk_category
from app.domain.data_quality import validate_customers, validate_payments

from app.domain.model import(
    prepare_model_data,
    train_model
)
from app.domain.training_data import build_training_data
from app.domain.risk import score_customer_record
from app.domain.portfolio import(
    score_portfolio,
    summarize_risk_bands,
    calculate_average_default_probability,
    find_high_risk_customers
)
from app.domain.model_service import(
    find_customer_by_id,
    prepare_model_service,
    get_model_info,
    get_model_status
)

from app.domain.model_evaluation import(
    calculate_evaluation_metrics,
    build_confusion_metrics
)

from app.data.cache_repository import(
    get_cached_risk,
    save_cached_risk
)
from app.domain.audit import create_audit_record
from app.data.audit_repository import(
    load_audit_records,
    create_audit_table,
    save_audit_record
)

setup_logging()
config = load_config()

app = FastAPI()

logger = logging.getLogger(__name__)

@app.get("/")
def home():
    # Return basic application information

    # Log when the home endpoint is called
    logger.info("Home endpoint called")

    return {
        "application_name": config["application_name"],
        "bank_name" : config["bank_name"],
        "currency" : config["currency"]
    }

@app.get("/health")
def health():
    # Simple end point to confirm the API is running

    # Log when the health endpoint is called
    logger.info("Health endpoint called")
    return{
        "application_name": config["application_name"],
        "status": "healthy"
    }

@app.get("/customers")
def get_customers():

    logger.info("Customers endpoint called")

    # Load customer and payment data
    _, customers,payments, _, _ = prepare_model_service()

    # Add credit utilization to each customer
    for customer in customers:
        add_credit_utilization(customer)

    # Add payment behaviour features
    add_payment_features_to_customers(
        customers,
        payments,
    )

    # Add risk score
    for customer in customers:
        customer["risk_score"] = calculate_risk_score(customer)
        customer["risk_category"] = get_risk_category(
            customer["risk_score"]
        )
        add_debt_to_income(customer)
        add_credit_utilization(customer)

    return customers

@app.get("/customers/{customer_id}")
def get_customer(customer_id: str):

    _,customers,_,_,_ = prepare_model_service()
    customer = find_customer_by_id(
        customers,
        customer_id
    )

    if customer is None:
        return {
            "error" : "Customer not found"
        }

    return customer

@app.get("/risk/{customer_id}")
def get_customer_risk(customer_id):

    if not re.fullmatch(r"C\d{3}", customer_id):
        raise HTTPException(
            status_code = 400,
            detail = "Invalid customer ID"
        )

    cached_result, cache_status = get_cached_risk(customer_id)

    if cached_result is not None:
        cached_result["cache_status"] = cache_status
        return cached_result

    model, customers,payments, x_test, y_test = prepare_model_service()

    customer = find_customer_by_id(
        customers,
        customer_id
    )

    if customer is None:
        raise HTTPException(
            status_code = 404,
            detail = "Invalid customer ID"
        )

    risk_result = score_customer_record(
        model,
        customer,
        payments
    )

    audit_record = create_audit_record(
        customer_id,
        risk_result
    )

    create_audit_table()
    save_audit_record(audit_record)
    
    risk_result["audit"] = audit_record

    save_cached_risk(
        customer_id,
        risk_result
    )

    risk_result["cache_status"] = cache_status

    return risk_result


@app.get("/data-quality")
def get_data_quality():

    _, customers,payments, _, _ = prepare_model_service()

    # Run our existing validation rules
    customer_errors = validate_customers(customers)
    payment_errors = validate_payments(payments)

    logger.info("Data quality endpoint called")

    return{
        "customer_errors": customer_errors,
        "payment_errors": payment_errors
    }

@app.get("/portfolio")
def get_portfolio():

    model, customers,payments, x_test, y_test = prepare_model_service()

    risk_results = score_portfolio(
        model,
        customers,
        payments
    )

    return {
        "total_customers": len(risk_results),
        "risk_bands": summarize_risk_bands(risk_results),
        "average_default_probability":
            calculate_average_default_probability(risk_results),
        "high_risk_customers":
            find_high_risk_customers(risk_results)
    }

@app.get("/model-evaluation")
def get_model_evaluation():

    model_info = get_model_info()
    model, customers,payments, x_test, y_test = prepare_model_service()
    metrics = calculate_evaluation_metrics(
        model,
        x_test,
        y_test
    )

    confusion = build_confusion_metrics(
        model,
        x_test,
        y_test
    )

    return {
        "model": model_info,
        "metrics": metrics,
        "confusion_metrics": confusion
    }

@app.get("/audit")
def get_audit_records():

    return load_audit_records()

@app.get("/model-status")
def get_current_model_status():
    return get_model_status()
