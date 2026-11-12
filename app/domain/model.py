from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, roc_auc_score
from app.core.config import load_config

def prepare_model_data(training_data):
    # Features used by the credit-risk model
    features = []

    # Historical outcome the model will learn to predict
    targets = []

    for record in training_data:
        features.append([
            record["credit_utilization"],
            record["debt_to_income"],
            record["late_payment_ratio"]
        ])

        targets.append(record["defaulted"])

    return features, targets

def train_model(features, targets):
    # Keep some historical data aside for independent evaluation
    x_train, x_test, y_train, y_test = train_test_split(
            features,
            targets,
            test_size = 0.2,
            random_state = 42,
            stratify = targets
            )

    # Train our first probability-of-default model
    model = LogisticRegression()

    model.fit(x_train,y_train)

    return model, x_test, y_test

def evaluate_model(model, x_test,y_test):
    # Predict default probabilities for unseen customers
    default_probabilities = model.predict_proba(x_test)[:, 1]

    # Convert probabilities into 0/1 predictions
    predictions = model.predict(x_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    roc_auc = roc_auc_score(
        y_test,
        default_probabilities
    )

    return {
        "accuracy": accuracy,
        "roc_auc": roc_auc
    }

def predict_default_probability(model, features):
    # Probability for class 1 means probability of default
    probabilities = model.predict_proba([features])

    return float(probabilities[0][1])

def get_risk_band(default_probability):
    # Read configurable risk thresholds
    config = load_config()

    medium_threshold = config["risk_thresholds"]["medium"]
    high_threshold = config["risk_thresholds"]["high"]

    if default_probability >= high_threshold:
        return "HIGH"

    if default_probability >= medium_threshold:
        return "MEDIUM"

    return "LOW"
