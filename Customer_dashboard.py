import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:5000"

if "user_name" in st.session_state:
    name = st.session_state['user_name']
    
st.title(f"Hi {name}! Welcome to Store!")

retailer, branch = st.columns(2)

response = requests.get(f"{BASE_URL}/get_providers")
if response.status_code == 200:
    provider_options = response.json()  # List of provider document names
else:
    provider_options = ["Error fetching data"]

with retailer:
    retailer_option = st.selectbox("Select retailer:",provider_options)
    st.write(f"You selected {retailer_option}")


# Fetch branches dynamically based on selected provider
if retailer_option and retailer_option != "Error fetching providers":
    response_branches = requests.get(f"{BASE_URL}/{retailer_option}")
    
    if response_branches.status_code == 200:
        branch_options = response_branches.json()
    else:
        branch_options = ["No branches found"]

    # Branch Dropdown
    with branch:    
        selected_branch = st.selectbox("Choose a Branch:", branch_options)
    
        st.write(f"Selected: {retailer_option} -> {selected_branch}")
    
