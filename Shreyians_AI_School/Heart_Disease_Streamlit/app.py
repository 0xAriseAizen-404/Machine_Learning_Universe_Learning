import streamlit as st
import pandas as pd
import joblib

xgb_model = joblib.load("XGB_heart.pkl")
rf_model = joblib.load("RF_heart.pkl")
lr_model = joblib.load("LogR_heart.pkl")

scaler = joblib.load("scaler.pkl")
expected_columns = joblib.load("X_columns.pkl")

model_choice = st.selectbox(
    "Choose Model",
    ["XGBoost", "Random Forest", "Logistic Regression"]
)

if model_choice == "XGBoost":
    model = xgb_model
elif model_choice == "Random Forest":
    model = rf_model
else:
    model = lr_model

st.title("Heart Stroke Prediction")
st.markdown("Provide the following details")

age = st.slider("Age", 18, 100, 40)
sex = st.selectbox("Sex", ['M', 'F'])
chest_pain = st.selectbox("Chest Pain Type", ["ATA", "NAP", "TA", "ASY"])
resting_bp = st.number_input("Resting BP (mm Hg)", 80, 200, 120)
cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, 200)
fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", [0, 1])
resting_ecg = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"])
max_hr = st.slider("Max Heart Rate", 60, 220, 150)
exercise_angina = st.selectbox("Exercise-Induced Angina", ["Y", "N"])
oldpeak = st.slider("Oldpeak (ST Depression)", 0.0, 6.0, 1.0)
st_slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

if st.button("Predict"):
    input_dict = {
        'Age': age,
        'RestingBP': resting_bp,
        'Cholesterol': cholesterol,
        'FastingBS': fasting_bs,
        'MaxHR': max_hr,
        'Oldpeak': oldpeak,
        
        'Sex_' + sex: 1,
        'ChestPainType_' + chest_pain: 1,
        'RestingECG_' + resting_ecg: 1,
        'ExerciseAngina_' + exercise_angina: 1,
        'ST_Slope_' + st_slope: 1,
    }

    input_df = pd.DataFrame([input_dict])

    # input_df['Sex_M'] = 1 if sex == 'M' else 0

    # input_df['ChestPainType_ATA'] = 1 if chest_pain == 'ATA' else 0
    # input_df['ChestPainType_NAP'] = 1 if chest_pain == 'NAP' else 0
    # input_df['ChestPainType_TA'] = 1 if chest_pain == 'TA' else 0

    # input_df['ExerciseAngina_Y'] = 1 if exercise_angina == 'Y' else 0

    # input_df['ST_Slope_Flat'] = 1 if st_slope == 'Flat' else 0
    # input_df['ST_Slope_Up'] = 1 if st_slope == 'Up' else 0

    for col in expected_columns:
        if col not in input_df.columns:
            input_df[col] = 0

    input_df = input_df[expected_columns]

    numeric_cols = ['Age', 'RestingBP', 'Cholesterol', 'MaxHR', 'Oldpeak']
    input_df[numeric_cols] = scaler.transform(input_df[numeric_cols])

    prediction = model.predict(input_df)[0]
    prob = model.predict_proba(input_df)[0][1]

    if prediction == 1:
        st.error(f"High Risk of Heart Disease ⚠️ (Probability: {prob:.2f})")
    else:
        st.success(f"Low Risk of Heart Disease ✅ (Probability: {prob:.2f})")

"""
🟢 Test Case 1 — Low Risk (should predict 0)

Use a generally healthy profile:

Age → 35
Sex → F
Chest Pain → ATA
Resting BP → 110
Cholesterol → 180
Fasting BS → 0
Resting ECG → Normal
Max HR → 170
Exercise Angina → N
Oldpeak → 0.0
ST Slope → Up

👉 Expected: Low Risk

🔴 Test Case 2 — High Risk (should predict 1)

Classic high-risk profile:

Age → 60
Sex → M
Chest Pain → ASY
Resting BP → 150
Cholesterol → 300
Fasting BS → 1
Resting ECG → ST
Max HR → 110
Exercise Angina → Y
Oldpeak → 3.5
ST Slope → Flat

👉 Expected: High Risk

🟡 Test Case 3 — Borderline Case

This is where models may disagree:

Age → 50
Sex → M
Chest Pain → NAP
Resting BP → 130
Cholesterol → 240
Fasting BS → 0
Resting ECG → Normal
Max HR → 140
Exercise Angina → N
Oldpeak → 1.5
ST Slope → Flat

👉 Expected: Could go either way

Good for testing differences between XGBoost / RF / LR
"""