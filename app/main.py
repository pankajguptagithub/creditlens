from fastapi import FastAPI
from app.core.config import load_config

config = load_config()
app = FastAPI()

@app.get("/")
def home():
    # Return basic application information
    return {
        "application_name": config["application_name"],
        "bank_name" : config["bank_name"],
        "currency" : config["currency"]
    }
