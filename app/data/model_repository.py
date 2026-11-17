import os
import pickle

from app.core.config import load_config

def get_model_path():
    
    config = load_config()

    model_name = config["model"]["name"]
    model_version = config["model"]["version"]

    return f"models/{model_name}_v{model_version}.pk1"

def save_model(model, x_test,y_test):
    model_path = get_model_path()

    os.makedirs("models", exist_ok=True)

    model_bundle = {
        "model": model,
        "x_test": x_test,
        "y_test": y_test,
    }

    with open(model_path, "wb") as file:
        pickle.dump(model, file)

def load_model():
    model_path = get_model_path()

    if not os.path.exists(model_path):
        return None

    with open(model_path,"rb") as file:
        model_bundle = pickle.load(file)

    # Older artifacts contained only the trained model
    # Ignore them so CreditLens can recreate the current bundle format 
    if not isinstance(model_bundle,dict):
        return None

    return model_bundle

def model_exists():
    return os.path.exists(get_model_path())
