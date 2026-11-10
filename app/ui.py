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


customers_response = requests.get(
    config["api_base_url"] + "/customers"
)

customers = customers_response.json()

st.subheader("Customers")

st.dataframe(customers)

#data_quality_response = requests.get(
#    config["api_base_url"] + "/data-quality"
#)
#
#data_quality = data_quality_response.json()
#print(data_quality)
#
#customer_errors = data_quality["customer_errors"]
#payment_errors = data_quality["payment_errors"]
#
#if not customer_errors and not payment_errors:
#    st.success("Data Quality: Passed")
#else:
#    st.error("Data Quality: Failed")




