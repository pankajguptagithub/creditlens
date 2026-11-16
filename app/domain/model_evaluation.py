from sklearn.metrics import(
    accuracy_score,
    brier_score_loss,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score
)

def calculate_evaluation_metrics(model, x_test,y_test):
    # Generate class predictions and probability-of-default predictions
    predictions = model.predict(x_test)
    default_probabilities = model.predict_proba(x_test)[:,1]

    metrics = {
        "accuracy": accuracy_score(y_test,predictions),
        "precision": precision_score(y_test,predictions,zero_division=0),
        "recall": recall_score(y_test,predictions, zero_division=0),
        "f1": f1_score(y_test,predictions, zero_division=0),
        "roc_auc": roc_auc_score(y_test,default_probabilities),
        "brier_score": brier_score_loss(y_test,default_probabilities)
    }

    return metrics

def build_confusion_metrics(model,x_test,y_test):
    # Return TN,FP,FN and TP values in a redable structure
    predictions = model.predict(x_test)
    matrix = confusion_matrix(y_test,predictions)

    true_negative, false_positive, false_negative, true_positive = matrix.ravel()

    return {
        "true_negative": int(true_negative),
        "false_positive": int(false_positive),
        "false_negative": int(false_negative),
        "true_positive": int(true_positive)
    }
