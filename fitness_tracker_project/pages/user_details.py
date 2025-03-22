import streamlit as st
import json
import os
import base64
import time

# Path to the uploaded image
bg_image_path = "images/user.png"

# Load and encode image to base64
with open(bg_image_path, "rb") as img_file:
    bg_image_encoded = base64.b64encode(img_file.read()).decode()

# Custom CSS for Enhanced Styling
# Updated CSS with scrollable background and enhanced styles
page_bg_img = f"""
<style>
    /* Scrollable Background */
    [data-testid="stAppViewContainer"] {{
        background: url('data:image/png;base64,{bg_image_encoded}') repeat center center;
        background-size: cover;
        overflow-y: auto; /* Allows the background to scroll with content */
    }}
    /* Content Box with White Background */
    [data-testid="stAppViewContainer"] > .main {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 10px;
        max-width: 700px;
        margin: auto;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }}
    /* Sidebar Background */
    [data-testid="stSidebar"] {{
        background-color: #f0f0f0;
    }}
    /* Header Section */
    [data-testid="stHeader"] {{
        background: rgba(0, 0, 0, 0);
    }}
    
    /* Headings */
    h1, h2, h3 {{
        color: #222;
        font-size: 1.8rem; /* Increased size */
        font-weight: bold;
    }}
    h1 {{
    color: #1E3A8A;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
}}
    /* Labels and Paragraphs */
    p, label {{
        color: #222;
        font-size: 1.2rem; /* Slightly larger font for better readability */
        font-weight: 500;
    }}
    button {{
    background-color: #4A90E2 !important;
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
   

    .custom-label {{
        font-size:18px; /* Increase font size */
        color: #333; /* Optional: Darker text color */
    }}
</style>
"""


# Inject the background CSS
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

# Page Title and Description
st.title("📝 Personal Information Details")
st.write("Please enter your fitness details below to continue.")

# User Inputs
with st.container():
   st.markdown('<div class="custom-label">Age</div>', unsafe_allow_html=True)
age = st.number_input("", min_value=10, max_value=100, step=1, value=None)

st.markdown('<div class="custom-label">Weight (kg)</div>', unsafe_allow_html=True)
weight = st.number_input("", min_value=30.0, max_value=200.0, step=0.1, value=None)

st.markdown('<div class="custom-label">Heart Rate (bpm)</div>', unsafe_allow_html=True)
heart_rate = st.number_input("", min_value=40, max_value=200, step=1, value=None)

st.markdown('<div class="custom-label">Height (cm)</div>', unsafe_allow_html=True)
height = st.number_input("", min_value=100, max_value=250, step=1, value=None)

st.markdown('<div class="custom-label">Gender</div>', unsafe_allow_html=True)
gender = st.selectbox("", ["", "Male", "Female", "Other"], index=0)

st.markdown('<div class="custom-label">Duration (minutes)</div>', unsafe_allow_html=True)
duration = st.number_input("", min_value=5, max_value=300, step=5, value=None)

st.markdown('<div class="custom-label">Body Temperature (°C)</div>', unsafe_allow_html=True)
body_temp = st.slider("", min_value=35.0, max_value=42.0, step=0.1, value=35.0)

st.markdown('<div class="custom-label">Target Weight to Reduce (kg)</div>', unsafe_allow_html=True)
target_weight_loss = st.number_input("", min_value=0.0, max_value=50.0, step=0.1, value=None)

# Path to user details JSON file
DETAILS_FILE = "user_details.json"

# Function to load existing user details
def load_user_details():
    if os.path.exists(DETAILS_FILE):
        with open(DETAILS_FILE, "r") as file:
            return json.load(file)
    return {"users": []}

# Function to save user details
def save_user_details(user_data):
    data = load_user_details()
    data["users"].append(user_data)
    with open(DETAILS_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Submit Button
if st.button("Submit"):
    if (
        age is None
        or weight is None
        or heart_rate is None
        or height is None
        or duration is None
        or gender == ""
    ):
        st.error("❌ Please fill in all required fields!")
    else:
        user_data = {
            "age": age,
            "weight": weight,
            "heart_rate": heart_rate,
            "height": height,
            "gender": gender,
            "duration": duration,
            "body_temp": body_temp,
            "target_weight_loss": target_weight_loss,
        }
        save_user_details(user_data)

        # Save values in session state
        st.session_state.update(user_data)
        
        
        #st.page_link("pages/summary.py", label="Go to Summary")
        time.sleep(1)  # Wait for 3 seconds
        st.success("✅ Your details have been saved successfully!")
        st.switch_page("pages/summary.py")

# Back Button
if st.button("🔙 Go Back"):
    st.switch_page("pages/login.py")
