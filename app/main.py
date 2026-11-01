import logging
from fastapi import FastAPI

from app.core.config import load_config
from app.core.logging_config import setup_logging

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
