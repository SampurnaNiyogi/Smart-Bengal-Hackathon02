import streamlit as st

if "user_name" in st.session_state:
    st.title(f"Hi {st.session_state['user_name']}! Welcome to Store!")