import streamlit as st
import json
import re
import os
import time
import base64

# Path to the uploaded image
bg_image_path = "images/login.png"

# Load and encode image to base64
with open(bg_image_path, "rb") as img_file:
    bg_image_encoded = base64.b64encode(img_file.read()).decode()

# Custom CSS for Enhanced Styling with Background Image
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background: url('data:image/png;base64,{bg_image_encoded}') no-repeat center center fixed;
    background-size: cover;
    overflow-y: auto;
}}
[data-testid="stHeader"] {{
    background: rgba(0, 0, 0, 0);
}}
[data-testid="stSidebar"] {{
        background-color: #f0f0f0;
    }}
.st-emotion-cache-10trblm {{
    background: rgba(255, 255, 255, 0.85);
    padding: 2rem;
    border-radius: 16px;
    box-shadow: 0px 5px 30px rgba(0, 0, 0, 0.2);
    max-width: 400px;
    margin: 5% auto;
    text-align: center;
}}
h1 {{
    color: #1E3A8A;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}}

input {{
    border-radius: 12px !important;
    border: 2px solid #1E3A8A !important;
    padding: 12px !important;
    width: 100% !important;
    background: #ffffff !important;
    color: #333333 !important;
    box-shadow: 0px 2px 10px rgba(0, 0, 0, 0.1);
}}
button {{
    background-color: #1E3A8A !important;
    color: #ffffff !important;
    padding: 12px 24px !important;
    border-radius: 8px !important;
    transition: all 0.3s ease-in-out !important;
    box-shadow: 0px 4px 12px rgba(30, 58, 138, 0.4);
}}
button:hover {{
    background-color: #3B82F6 !important;
    transform: scale(1.05);
}}

</style>
"""

# Apply CSS with background
st.markdown(page_bg_img, unsafe_allow_html=True)

# Custom CSS to hide sidebar
hide_sidebar = """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

# Title and Instructions
st.title("🔑 Login ")
st.write("Enter your credentials to login and explore the dashboard.")

# User Inputs
username = st.text_input("👤 Username (Max 20 characters)")
password = st.text_input("🔒 Password", type="password")

# Path for user data
DATA_FILE = "user_data.json"

# Function to load user data
def load_user_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {"users": []}

# Function for validating username
def is_valid_username(username):
    return bool(re.match(r"^[A-Za-z0-9_]{1,20}$", username))

# Function for validating password
def is_valid_password(password):
    return bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$", password))

# Function to verify user credentials
def validate_credentials(username, password):
    data = load_user_data()
    for user in data["users"]:
        if user["username"] == username and user["password"] == password:
            return True
    return False

# Function to check if username exists
def is_user_registered(username):
    data = load_user_data()
    for user in data["users"]:
        if user["username"] == username:
            return True
    return False

# Login Button with Validation
if st.button("🚀 Login"):
    if not username or not password:
        st.error("⚠️ Please enter both username and password.")
    elif not is_valid_username(username):
        st.error("⚠️ Username can only contain letters, numbers, and underscores (Max 20 characters).")
    elif not is_valid_password(password):
        st.error("⚠️ Password must be at least 8 characters and include:\n - 1 uppercase letter\n - 1 lowercase letter\n - 1 number\n - 1 special character (@, #, $, etc.)")
    elif validate_credentials(username, password):
        st.session_state["logged_in"] = True
        st.session_state["username"] = username
        st.success("✅ Logged in successfully! 🎉")
        st.switch_page("pages/user_details.py")
    elif not is_user_registered(username):
        st.error("❌ User not found. Please register first.")
        
        # Delay before redirecting to registration
        time.sleep(3)  # Wait for 3 seconds
        st.success("🔗 Redirecting to Registration Page...")
        st.switch_page("pages/register.py")
    else:
        st.error("❌ Incorrect password. Please try again or reset your password.")

# Go Back Button
if st.button("🔙 Go Back"):
    st.switch_page("logo.py")
