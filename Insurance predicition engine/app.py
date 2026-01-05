import streamlit as st
import pickle
import numpy as np

# 1. Load the Model
try:
    with open('insurance_model.pkl', 'rb') as f:
        model = pickle.load(f)
except FileNotFoundError:
    st.error("Error: 'insurance_model.pkl' not found. Make sure it's in the folder!")
    st.stop()

# 2. App Title
st.title("🏥 Medical Cost AI Predictor")
st.write("Enter patient details to generate a real-time insurance cost estimate.")

# 3. Sidebar Inputs (We need ALL 8 features now)
st.sidebar.header("Patient Data")

# Numeric Features
age = st.sidebar.slider("Age", 18, 100, 30)
bmi = st.sidebar.slider("BMI", 15.0, 50.0, 25.0)
children = st.sidebar.slider("Number of Children", 0, 5, 0)

# Categorical Features
sex_input = st.sidebar.selectbox("Sex", ["Female", "Male"])
smoker_input = st.sidebar.selectbox("Smoker Status", ["No", "Yes"])
region_input = st.sidebar.selectbox("Region", ["Northeast", "Northwest", "Southeast", "Southwest"])

# 4. Preprocessing (Converting words to the 8 numbers the model expects)
# Note: This assumes standard pd.get_dummies(drop_first=True) order.
# If your prediction is weird, the order might be different.

# Sex (1 = Male, 0 = Female)
sex_male = 1 if sex_input == "Male" else 0

# Smoker (1 = Yes, 0 = No)
smoker_yes = 1 if smoker_input == "Yes" else 0

# Region (One-Hot Encoding)
# We have 3 columns for 4 regions (Northeast is the baseline 0,0,0)
region_nw = 1 if region_input == "Northwest" else 0
region_se = 1 if region_input == "Southeast" else 0
region_sw = 1 if region_input == "Southwest" else 0

# 5. Prediction Logic
if st.sidebar.button("Calculate Risk"):
    # The Array: [Age, BMI, Children, Sex_Male, Smoker_Yes, Region_NW, Region_SE, Region_SW]
    # This must match your X_train.columns order EXACTLY.
    input_data = [[age, bmi, children, sex_male, smoker_yes, region_nw, region_se, region_sw]]

    try:
        prediction = model.predict(input_data)
        cost = prediction[0]

        st.subheader("Estimated Annual Cost")
        st.metric(label="USD", value=f"${cost:,.2f}")

        if cost > 20000:
            st.warning("⚠️ High Risk Profile.")
        else:
            st.success("✅ Standard Risk Profile.")

    except ValueError as e:
        st.error(f"Error: {e}")
        st.info("Tip: Run `print(X_train.columns)` in your notebook to see the exact column order required.")