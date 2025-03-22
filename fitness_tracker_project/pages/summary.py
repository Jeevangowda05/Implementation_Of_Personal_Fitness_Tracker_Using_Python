import streamlit as st
import pandas as pd
import os
import base64

# Path to the uploaded image
bg_image_path = "images/sum.png"

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
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st.title("📊 Personal Fitness Tracker Based on AI")

# Custom CSS to hide sidebar
hide_sidebar = """
    <style>
        [data-testid="stSidebar"] {
            display: none;
        }
    </style>
"""
st.markdown(hide_sidebar, unsafe_allow_html=True)

# Check if user details exist in session state
if "age" not in st.session_state:
    st.error("⚠️ No user data found! Please enter your details on the previous page.")
    st.stop()

# Retrieve user details
age = st.session_state.age
weight = st.session_state.weight
height = st.session_state.height
gender = st.session_state.gender
target_weight_loss = st.session_state.target_weight_loss
duration = st.session_state.duration
heart_rate = st.session_state.heart_rate
body_temp = st.session_state.body_temp

# Calculate BMI
height_m = height / 100
bmi = weight / (height_m ** 2)

# Calculate BMR based on gender
if gender == "Male":
    bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
elif gender == "Female":
    bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)
else:
    bmr = (88.36 + 447.6) / 2 + ((13.4 + 9.2) / 2 * weight) + ((4.8 + 3.1) / 2 * height) - ((5.7 + 4.3) / 2 * age)

# Display User Data
st.write(f"**👤 Age:** {age} years")
st.write(f"**⚖️ Weight:** {weight} kg")
st.write(f"**📏 Height:** {height} cm")
st.write(f"**🎯 Target Weight Loss:** {target_weight_loss} kg")
st.write(f"**⏳ Duration:** {duration} minutes")
st.write(f"**❤️ Heart Rate:** {heart_rate} bpm")
st.write(f"**🌡️ Body Temperature:** {body_temp} °C")

# Estimate total calories to burn for target weight loss
if "target_weight_loss" in st.session_state:
    total_calories_to_burn = target_weight_loss * 7700
    daily_deficit = 500
    weeks_to_lose_weight = total_calories_to_burn / (daily_deficit * 7)
    months_to_lose_weight = weeks_to_lose_weight / 4.33

    st.subheader("📉 Estimated Weight Loss Duration")
    st.write(
        f"💡 You can reach your target weight in approximately **{months_to_lose_weight:.1f} months** with a **{daily_deficit} kcal/day** deficit."
    )
    st.info("This is an estimate and may vary based on diet, exercise, and metabolism.")

# Display BMI
st.subheader("📌 Body Mass Index (BMI)")
st.write(f"**Your BMI:** {bmi:.2f}")

# Interpret BMI Category
if bmi < 18.5:
    bmi_category = "Underweight"
    st.warning("🔹 Underweight")
elif 18.5 <= bmi < 24.9:
    bmi_category = "Normal weight"
    st.success("✅ Normal weight")
elif 25 <= bmi < 29.9:
    bmi_category = "Overweight"
    st.warning("⚠️ Overweight")
else:
    bmi_category = "Obese"
    st.error("❌ Obese")

# Load CSV and compare user data
file_path = "data/users.csv"
if os.path.exists(file_path):
    df = pd.read_csv(file_path)

    # Check for exact match
    match = df[
        (df["Gender"] == gender)
        & (df["Age"] == age)
        & (df["Height"] == height)
        & (df["Weight"] == weight)
        & (df["Duration"] == duration)
        & (df["Heart_Rate"] == heart_rate)
        & (df["Body_Temp"] == body_temp)
    ]

    if not match.empty:
        st.success("🎯 Your details match a record in our database!")
        st.dataframe(match.drop(columns=["User_ID", "SLno"], errors="ignore"))
    else:
        # st.warning("⚠️ No exact match found in the dataset.")

        # Find top 5 closest matches
        df["score"] = (
            (df["Age"] - age).abs()
            + (df["Weight"] - weight).abs()
            + (df["Height"] - height).abs()
            + (df["Heart_Rate"] - heart_rate).abs()
            + (df["Body_Temp"] - body_temp).abs()
        )

        top_5_matches = df.nsmallest(5, "score").drop(
            columns=["User_ID", "SLno", "score"], errors="ignore"
        )

        if not top_5_matches.empty:
            st.subheader("🔍 Predicated Information of User Input")
            st.dataframe(top_5_matches)
        else:
            st.warning("⚠️ No close matches found.")

else:
    st.error("❌ User dataset CSV not found! Please ensure the file is in the 'data' folder.")

# Load and display top 3 diet recommendations based on BMI
diet_file_path = "data/diet_plan.csv"
if os.path.exists(diet_file_path):
    diet_df = pd.read_csv(diet_file_path)
    diet_recommendation = diet_df[diet_df["BMI_Category"] == bmi_category].head(3)

    if not diet_recommendation.empty:
        st.subheader(" Personalized Diet Recommendations")
        for index, row in diet_recommendation.iterrows():
            st.write(f"🍽️ **Food:** {row['Food']}")
            st.write(f"🔥 **Calories:** {row['Calories']} kcal")
            st.write(f"💪 **Protein:** {row['Protein']}")
            st.write(f"🛢️ **Fat:** {row['Fat']}")
            st.write(f"🍞 **Carbs:** {row['Carbs']}")
            st.markdown("---")
    else:
        st.warning("⚠️ No diet recommendations found for your BMI category.")
else:
    st.error("❌ Diet plan dataset not found!")

# Display BMR
st.subheader("🔥 Basal Metabolic Rate (BMR)")
st.write(f"**Your BMR:** {bmr:.2f} kcal/day")

st.info("BMR is the number of calories your body needs at rest to maintain basic functions.")

# Navigation Buttons
if st.button("🔙 Go Back"):
    st.page_link("pages/user_details.py", label="Go to User Details")
