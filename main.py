import streamlit as st
import time

st.title("Cashier Less Retail Shop")

status_placeholder = st.empty()


with status_placeholder.status("Loading......"):
    for i in range(1):
        time.sleep(1)  # Simulate a step taking time

status_placeholder.empty()

if "pages" not in st.session_state:
    st.session_state.page = "False"

# Show "Enter Store" button after loading is complete
if st.button("Enter Store"):
    st.switch_page("pages/Login.py")
    st.session_state.page = "Login"
    st.rerun()
