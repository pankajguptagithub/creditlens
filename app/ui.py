import requests
import streamlit as st

from app.core.config import load_config

config = load_config()

response = requests.get((config["api_base_url"]))

data = response.json()

st.title(data["application_name"])
st.subheader(data["bank_name"])

st.write("Currency:",data["currency"])
