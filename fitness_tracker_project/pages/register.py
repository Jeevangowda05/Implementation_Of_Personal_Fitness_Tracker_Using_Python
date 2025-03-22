import streamlit as st
import json
import re
import os
import time
import base64

# Path to the uploaded image
bg_image_path = "images/register_flipped.png"

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
.stAlert {{
    background: rgba(255, 255, 255, 0.9) !important;
    border-radius: 12px;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Title
st.title("📝 Register ")
st.write("Create a new account.")

# Custom CSS to hide sidebar
hide_sidebar = """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

# User Input Fields
new_username = st.text_input("New Username (Max 20 characters)")
new_password = st.text_input("New Password", type="password")

# Path to user data file
DATA_FILE = "user_data.json"

# Function to load user data
def load_user_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {"users": []}

# Function to save user data
def save_user_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Function to check if username already exists
def is_user_registered(username):
    data = load_user_data()
    for user in data["users"]:
        if user["username"] == username:
            return True
    return False

# Validation Functions
def is_valid_username(username):
    return bool(re.match(r"^[A-Za-z0-9_]{1,20}$", username))

def is_valid_password(password):
    return bool(re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&+=!]).{8,}$", password))

# Register Button Logic
if st.button("Register"):
    if not new_username or not new_password:
        st.error("⚠️ Please fill in all fields.")
    elif not is_valid_username(new_username):
        st.error("⚠️ Username can only contain letters, numbers, and underscores (Max 20 characters).")
    elif not is_valid_password(new_password):
        st.error("⚠️ Password must be at least 8 characters and contain: \n - 1 uppercase letter \n - 1 lowercase letter \n - 1 number \n - 1 special character (@, #, $, etc.)")
    elif is_user_registered(new_username):
        st.error("❌ Username already exists. Redirecting to login...")
        
        # Wait for 3 seconds before redirecting to login
        time.sleep(1.5)
        
        # Redirect to login page automatically
        st.switch_page("pages/login.py")

    else:
        # Register the new user
        data = load_user_data()
        data["users"].append({"username": new_username, "password": new_password})
        save_user_data(data)

        # Auto-login after registration
        st.session_state["logged_in"] = True
        st.session_state["username"] = new_username

        # Successful registration message
        st.success("🎉 Registration successful! Redirecting to login...")
        
        # Wait for 2 seconds before switching to login page
        time.sleep(1)
        st.switch_page("pages/login.py")

# Go Back Button
if st.button("🔙 Go Back"):
    st.switch_page("logo.py")

