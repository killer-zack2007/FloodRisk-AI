# FloodRisk AI

An interactive machine-learning based flood probability prediction dashboard.

## Project

FloodRisk AI predicts flood probability using 20 environmental,
infrastructure, governance, and human-impact factors.

## Machine Learning Model

- Algorithm: Linear Regression
- Training records: 1,117,957
- Input features: 20
- Validation R2: 0.844877
- Validation MAE: 0.015792
- Validation RMSE: 0.020080

## Features

- Flood probability prediction
- Risk classification
- Explainable model factors
- What-if scenario simulator
- Prediction history
- Responsive Streamlit dashboard

## Project Structure

Flood_Prediction/
├── app.py
├── models/
│   ├── flood_prediction_model.joblib
│   ├── feature_columns.json
│   └── model_metadata.json
├── src/
├── data/
├── outputs/
├── results/
├── requirements.txt
├── .gitignore
└── README.md

## Run Locally

pip install -r requirements.txt

streamlit run app.py

## Deployment

The application can be deployed using Streamlit Community Cloud
directly from GitHub.

## Important

The prediction is a machine-learning estimate based on the supplied
feature values. It should not be treated as an official flood warning
or a replacement for government or emergency information.
