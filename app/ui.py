import requests
import streamlit as st

from app.core.config import load_config

config = load_config()

response = requests.get((config["api_base_url"]))
data = response.json()

health_response = requests.get(
        config["api_base_url"] + "/health"
)
health_data = health_response.json()

st.title(data["application_name"])
st.subheader(data["bank_name"])

st.write("Currency:",data["currency"])
st.write("API Status:", health_data["status"])

data_quality_response = requests.get(
    config["api_base_url"] + "/data-quality"
)

data_quality = data_quality_response.json()

customer_errors = data_quality["customer_errors"]
payment_errors = data_quality["payment_errors"]

if not customer_errors and not payment_errors:
    st.success("Data Quality: Passed")
else:
    st.error("Data Quality: Failed")

customers_response = requests.get(
    config["api_base_url"] + "/customers"
)

customers = customers_response.json()

st.subheader("Customers")

st.dataframe(customers)

st.subheader("Borrower Risk")


customer_id = st.text_input("Customer ID")

if st.button("Analyze Risk"):
    risk_response = requests.get(
        config["api_base_url"] + "/risk/" + customer_id
    )

    risk_result = risk_response.json()

    if "error" in risk_result:
        st.error(risk_result["error"])
    else:
        st.write(
            "Probability of Default:",
            f"{risk_result['default_probability']:.2%}"
        )

        st.write(
                "Model:",
                risk_result["model_name"],
                "v" + risk_result["model_version"]
        )

        st.write(
            "Risk Band:",
            risk_result["risk_band"]
        )
        st.write(
            "Request ID:",
            risk_result["audit"]["request_id"]
        )

        st.write(
            "Scored At:",
            risk_result["audit"]["timestamp"]
        )

        st.write("Risk Reasons")

        for reason in risk_result["reasons"]:
            st.write("-",reason)

st.subheader("Portfolio Analytics")

portfolio_response = requests.get(
    config["api_base_url"] + "/portfolio"
)

portfolio = portfolio_response.json()

st.write(
    "Total Customers",
    portfolio["total_customers"],
)

st.write(
    "Average Probability of Default:",
    f"{portfolio['average_default_probability']:.2%}"
)

st.write("Risk Distribution:")

st.bar_chart(portfolio["risk_bands"])

st.write("High Risk Customers")

high_risk_customers = portfolio["high_risk_customers"]

if high_risk_customers:
    st.dataframe(high_risk_customers)
else:
    st.write("No high-risk customers found")

st.subheader("Model evaluation")

evaluation_response = requests.get(
        config["api_base_url"] + "/model-evaluation"
)

evaluation = evaluation_response.json()
model_info = evaluation["model"]
metrics = evaluation["metrics"]
confusion = evaluation["confusion_metrics"]

st.write(
    "Model:",
    model_info["name"],
    "v" + model_info["version"]
)
st.write("Accuracy:", f"{metrics['accuracy']:.2%}")
st.write("Precision:",f"{metrics['precision']:.2%}")
st.write("Recall:",f"{metrics['recall']:.2%}")
st.write("F1 Score:",f"{metrics['f1']:.2%}")
st.write("ROC-AUC:",f"{metrics['roc_auc']:.3f}")
st.write("Brier Score:",f"{metrics['brier_score']:.2%}")

st.write("Confusion Metrics")
st.json(confusion)

st.subheader("Recent Risk Audit")

audit_response = requests.get(
    config["api_base_url"] + "/audit"
)

audit_records = audit_response.json()

if audit_records:
    st.dataframe(
        audit_records[:10]
    )
else:
    st.write("No audit records found")
