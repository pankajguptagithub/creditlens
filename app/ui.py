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
            risk_result["default_probability"]
        )

        st.write(
            "Risk Band:",
            risk_result["risk_band"]
        )

        st.write("Risk Reasons")

        for reason in risk_result["reasons"]:
            st.write("-",reason)
