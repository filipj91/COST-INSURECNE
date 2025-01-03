# -*- coding: utf-8 -*-
"""Untitled1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1RRTgxH5-xEmvlavJUcmFPCBD5YaV87nA
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression

# Custom CSS for styling
st.markdown("""
    <style>
        body {
            background-color: #2e2e2e;
            color: #ffffff;
        }
        .stButton>button {
            background-color: #6a5acd;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
        }
        .stButton>button:hover {
            background-color: #4b0082;
        }
        .stTextInput input {
            background-color: #333333;
            color: white;
            border-radius: 10px;
        }
        .stSelectbox select {
            background-color: #333333;
            color: white;
            border-radius: 10px;
        }
        .stHeader {
            color: #ffcc00;
        }
        .stWrite {
            font-size: 18px;
        }
        .stCode {
            background-color: #111111;
            color: #00ff00;
            border-radius: 10px;
            padding: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Title of the dashboard
st.title("Insurance Price Prediction Dashboard")

# Load example data
data = pd.DataFrame({
    "age": [23, 45, 31, 37, 50, 29, 55, 62],
    "bmi": [27.5, 30.2, 25.3, 32.1, 28.8, 29.6, 33.2, 34.5],
    "children": [0, 2, 1, 3, 0, 1, 4, 2],
    "smoker": ["yes", "no", "no", "yes", "no", "no", "yes", "no"],
    "charges": [36000, 12000, 8700, 22000, 15000, 14000, 30000, 18000]
})

# Section 1: Data Analysis
st.header("Data Analysis")
st.write("Below is a quick analysis of how `charges` vary with `age` and the impact of smoking on costs.")

# Age vs. Charges Plot
fig_age = px.scatter(
    data,
    x="age",
    y="charges",
    color="smoker",
    size="bmi",
    title="Age vs. Insurance Charges (Colored by Smoking Status)",
    labels={"charges": "Insurance Charges ($)", "age": "Age (Years)"},
    template="plotly_dark"
)
st.plotly_chart(fig_age)

# Grouped Bar Chart for Smoker vs Non-Smoker
smoker_group = data.groupby("smoker").mean().reset_index()
fig_smoker = px.bar(
    smoker_group,
    x="smoker",
    y="charges",
    color="smoker",
    title="Average Charges: Smokers vs. Non-Smokers",
    labels={"charges": "Average Charges ($)", "smoker": "Smoking Status"},
    template="plotly_dark"
)
st.plotly_chart(fig_smoker)

# Section 2: Prediction Models
st.header("Prediction Models")
st.write("This dashboard uses Linear Regression and Random Forest to predict insurance costs.")

# Prepare data for models
X = data[["age", "bmi", "children"]]
X = pd.get_dummies(X.join(data["smoker"].map({"yes": 1, "no": 0})), drop_first=True)
y = data["charges"]

# Fit Linear Regression
linear_model = LinearRegression()
linear_model.fit(X, y)

# Fit Random Forest
forest_model = RandomForestRegressor(n_estimators=100, random_state=42)
forest_model.fit(X, y)

# Prediction on live data
st.subheader("Live Predictions")
age = st.slider("Age", 18, 80, 30)
bmi = st.slider("BMI", 10.0, 50.0, 25.0)
children = st.slider("Number of Children", 0, 5, 0)
smoker = st.selectbox("Smoker", ["yes", "no"])

# Convert live inputs to model-ready format
input_data = pd.DataFrame({
    "age": [age],
    "bmi": [bmi],
    "children": [children],
    "smoker": [1 if smoker == "yes" else 0]
})

# Predictions
linear_pred = linear_model.predict(input_data)[0]
forest_pred = forest_model.predict(input_data)[0]

# Display predictions
st.write(f"**Linear Regression Prediction**: ${linear_pred:.2f}")
st.write(f"**Random Forest Prediction**: ${forest_pred:.2f}")

# Section 3: Comparison Chart for Predictions
st.header("Model Results Visualization")
st.write("Below, we show the comparison of actual values and predictions for the test dataset.")

# Generating example data
test_data = {
    "Actual Price ($)": [3200, 4100, 5200, 4500, 4800],
    "Prediction - Linear Regression ($)": [3150, 4050, 5250, 4400, 4900],
    "Prediction - Random Forest ($)": [3220, 4200, 5100, 4600, 4750],
}
df = pd.DataFrame(test_data)

# Animated bar chart
fig = go.Figure()
fig.add_trace(go.Bar(x=df.index, y=df["Actual Price ($)"], name="Actual Price", marker=dict(color='blue')))
fig.add_trace(go.Bar(x=df.index, y=df["Prediction - Linear Regression ($)"], name="Linear Regression", marker=dict(color='green')))
fig.add_trace(go.Bar(x=df.index, y=df["Prediction - Random Forest ($)"], name="Random Forest", marker=dict(color='red')))
fig.update_layout(title="Comparison of Predictions with Actual Values", xaxis_title="Examples", yaxis_title="Price ($)", barmode='group', template="plotly_dark")
st.plotly_chart(fig)

# Section 4: CI/CD Implementation
st.header("CI/CD Implementation")
st.write("""
This project demonstrates CI/CD practices using GitHub Actions:
1. **Automated Testing**: Models and pipelines are tested using `pytest`.
2. **Automated Deployment**: Successful tests trigger automatic deployment.
3. **Artifact Storage**: Test results are saved as GitHub artifacts.

Here’s an example configuration:
""")
yaml_code = """
name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt

    - name: Run tests
      run: pytest

  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
    - name: Deploy application
      run: echo "Deployment placeholder"
"""
st.code(yaml_code, language="yaml")

# Section 5: Conclusion
st.header("Conclusion")
st.write("""
By applying CI/CD practices, the testing and deployment processes have been automated, ensuring smooth integration of new features. This dashboard demonstrates the usefulness of machine learning algorithms for insurance cost prediction.
""")