import streamlit as st
import firebase_admin
from firebase_admin import credentials, firestore
import time


# Load Firebase credentials (Use a service account JSON file)
if not firebase_admin._apps:
    cred = credentials.Certificate("sbh25-2d8ba-firebase-adminsdk-fbsvc-d4cce1ee41.json")  # Update with your file path
    firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

if "user_registered" not in st.session_state:
    st.session_state.user_registered = None

if "page" not in st.session_state:
    st.session_state.page = "customer_login"

def login_page():
    st.title("Login/Sign Up")
    if st.button("Sign In"):
        st.session_state.user_registered = "Existing"
        st.rerun()

    elif st.button("Sign Up"):
        st.session_state.user_registered = "New User"
        st.rerun()
    
# Add user data to Firestore
def add_user(name, email):
    users_ref = db.collection("users")
    users_ref.add({"name": name, "email": email})  # Store data in Firestore
    st.session_state.user_registered = True  # Mark registration as complete
    return


def register():
    st.title("Sign Up")
    st.subheader("New User Sign Up")
    name = st.text_input("Enter Name")
    email = st.text_input("Enter Email")
    if st.button("Sign Up"):
        add_user(name, email)
        st.success(f"User {name} added successfully!")
        st.session_state.page = "consumer_dashboard"
        st.session_state.user_registered = "Existing"
        status_placeholder = st.empty()
        with status_placeholder.status("Loading......"):
            for i in range(1):
                time.sleep(1)  # Simulate a step taking time

        status_placeholder.empty()
        st.rerun()
        

def authenticate():
    st.title("Sign In")
    u_name = st.text_input("Enter Name")
    email = st.text_input("Enter Email")
    if st.button("Sign In"):
        st.session_state["user_name"] = u_name
        st.switch_page("pages/Customer_dashboard.py")


if st.session_state.user_registered is None:
    login_page()
elif st.session_state.user_registered == "New User":
    register()
elif st.session_state.user_registered == "Existing":
    authenticate()
