import streamlit as st



# Custom CSS for styling
st.markdown(
    """
    <style>
        .stApp {
            background: linear-gradient(to right, #141E30, #243B55);
            color: white;
            text-align: center;
            font-family: 'Times NeW Roman', sans-serif;
        }
        [data-testid="stHeader"] {
    background: rgba(0, 0, 0, 0);
}
        .header-text {
            font-family: 'Times NeW Roman';
            font-size: 40px;
            font-weight: bold;
            color: #f4a261;
            text-align: center;
            margin-top: 25px;
        }
        
        
        .stButton>button {
            background-color: #f4a261 !important;
            color: #ffffff !important;
            border-radius: 10px !important;
            padding: 10px 30px !important;
            font-size: 18px !important;
            font-weight: bold !important;
        }
        .stButton>button:hover {
            background-color: #e76f51 !important;
        }button:hover {
    background-color: #3B82F6 !important; /* light blue */
}
    </style>
    """,
    unsafe_allow_html=True
)

# Add fitness logo
st.image("https://cdn-icons-png.flaticon.com/512/3589/3589131.png", width=200)

# Title
st.markdown("<div class='header-text'>Personal Fitness Tracker Based On AI</div>", unsafe_allow_html=True)
# Custom CSS to hide sidebar
hide_sidebar = """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)
# Navigation buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("🔑 Login"):
        st.query_params["page"] = "login"

with col2:
    if st.button("📝 Register"):
        st.query_params["page"] = "register"

# Check query params and redirect
if "page" in st.query_params:
    if st.query_params["page"] == "login":
        st.switch_page("pages/login.py")
    elif st.query_params["page"] == "register":
        st.switch_page("pages/register.py")

st.write(
    """
    Welcome to your personal fitness journey! 🎯  
    Whether you're aiming to lose weight, build muscle, or increase endurance, we've got you covered.  
    Track your daily progress, analyze insights, and stay motivated with personalized recommendations.  
    Set realistic goals, monitor key health metrics, and stay consistent as you transform your lifestyle. 💪  
    Let's get started and achieve your fitness goals together! 🚀
    """
)

