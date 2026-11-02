import logging
from fastapi import FastAPI

from app.core.config import load_config
from app.core.logging_config import setup_logging
from app.data.customer_repository import load_customers
from app.data.payment_repository import load_payments
from app.domain.features import (
        add_credit_utilization,
        add_payment_features_to_customers
)        
from app.domain.risk import calculate_risk_score, get_risk_category

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
    customers = load_customers()
    payments = load_payments()

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

    return customers

@app.get("/customers/{customer_id}")
def get_customer(customer_id: str):
    customers = get_customers()

    for customer in customers:
        if customer["customer_id"] == customer_id:
            return customer

    return {"error": "Customer not found"}

@app.get("/risk/{customer_id}")
def get_customer_risk(customer_id: str):
    customers = get_customers()

    for customer in customers:
        if customer["customer_id"] == customer_id:
            return{
                "customer_id": customer["customer_id"],
                "risk_score": customer["risk_score"],
                "risk_category": customer["risk_category"],
            }
    return {"error": "Customer not found"}





















