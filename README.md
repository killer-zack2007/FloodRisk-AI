FloodGuard AI — Flood Risk & Response Decision System

An interactive Streamlit prototype that estimates dataset-based flood probability using 20 environmental, infrastructure, governance, and human-impact features.

«Important: FloodGuard AI is an educational decision-support prototype. It is not an official flood-warning system and has not been validated as a real-world live flood forecast. Always follow official meteorological alerts and emergency-service guidance.»

Project Overview

FloodGuard AI uses a Linear Regression machine-learning model to estimate the "FloodProbability" target from user-provided feature values.

The project aims to combine machine-learning predictions with risk classification, scenario exploration, and decision-support concepts in an interactive dashboard.

Machine Learning Model

Property| Details
Algorithm| Linear Regression
Prediction target| "FloodProbability"
Input features| 20
Dataset size| 1,117,957 rows
Saved model| "models/flood_prediction_model.joblib"
Feature configuration| "models/feature_columns.json"
Model metadata| "models/model_metadata.json"

Model Validation Results

A temporary Linear Regression model was trained on 80% of the dataset and evaluated on the remaining 20%. The split used "random_state=42".

Evaluation metric| Result
Training rows| 894,365
Validation rows| 223,592
Mean Absolute Error (MAE)| 0.015792
Root Mean Squared Error (RMSE)| 0.020080
R² score| 0.844877
Predictions below 0| 0
Predictions above 1| 0

Interpretation:

- MAE of 0.015792 corresponds to approximately 1.58 percentage points on the probability scale.
- RMSE of 0.020080 corresponds to approximately 2.01 percentage points.
- R² of 0.844877 indicates that the model explains approximately 84.49% of the target variance in this evaluation.

The validation model was temporary and did not overwrite the saved production model. These results measure performance on a held-out portion of the supplied dataset; they do not establish real-world flood forecasting accuracy or probability calibration against observed flood events.

Input Features

The model uses these 20 features:

1. "MonsoonIntensity"
2. "TopographyDrainage"
3. "RiverManagement"
4. "Deforestation"
5. "Urbanization"
6. "ClimateChange"
7. "DamsQuality"
8. "Siltation"
9. "AgriculturalPractices"
10. "Encroachments"
11. "IneffectiveDisasterPreparedness"
12. "DrainageSystems"
13. "CoastalVulnerability"
14. "Landslides"
15. "Watersheds"
16. "DeterioratingInfrastructure"
17. "PopulationScore"
18. "WetlandLoss"
19. "InadequatePlanning"
20. "PoliticalFactors"

The feature order must match "models/feature_columns.json".

Feature meanings, scales, and directions should be checked against the source dataset before interpreting inputs as real-world measurements. A model coefficient's direction alone does not establish the physical effect of a factor on flooding.

Risk Classification

The current prototype converts the model output to a percentage by multiplying it by 100 and applies these application-defined thresholds:

Risk category| Score
LOW| Below 25
MODERATE| 25 to below 50
HIGH| 50 to below 75
VERY HIGH| 75 or above

These thresholds are prototype display rules, not official flood-warning thresholds.

Observed Score Distribution

The following percentiles were calculated from 223,592 holdout predictions.

Percentile| Predicted score
Minimum| 30.25
5th percentile| 43.23
10th percentile| 45.49
25th percentile| 47.70
Median| 50.00
75th percentile| 53.41
90th percentile| 56.76
95th percentile| 57.93
99th percentile| 62.97
Maximum| 75.42

With the current thresholds, the holdout predictions were distributed as follows:

Category| Number of predictions
LOW| 0
MODERATE| 111,811
HIGH| 111,778
VERY HIGH| 3

This shows that predictions are concentrated around the MODERATE and HIGH categories. These categories should not be interpreted as calibrated real-world flood severity levels. Any future threshold changes should be supported by suitable validation data and a documented methodology.

Features and Dashboard Capabilities

The prototype is designed to support:

- Flood probability estimation from 20 input features
- Risk category display
- Input-factor exploration
- What-if scenario simulation
- Prediction history
- Interactive Streamlit dashboard

The behavior of each feature depends on the implementation in the repository. Live weather or location information should not be described as directly affecting the machine-learning prediction unless the integration and feature mapping have been implemented and validated.

Project Structure

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

Installation and Usage

1. Clone the repository

git clone https://github.com/killer-zack2007/FloodRisk-AI.git
cd FloodRisk-AI

2. Install dependencies

pip install -r requirements.txt

3. Start the Streamlit application

streamlit run app.py

Ensure that the model files exist at the paths expected by the application and that all required dependencies are installed.

Limitations

- The model has been evaluated on the supplied dataset, not independently validated against real-world flood events.
- A strong R² score does not mean that individual predictions are accurate by that percentage.
- Linear Regression can produce values outside the 0–1 probability range for unusual or out-of-distribution inputs.
- Feature importance and direction require careful interpretation.
- Risk-category thresholds are prototype rules, not official warnings.
- Live environmental data must be independently validated before it is used as a model input.
- The model's estimated probabilities should not be assumed to be calibrated real-world probabilities.

Future Improvements

- Evaluate the model on independent external datasets.
- Test against documented flood events and observed outcomes.
- Evaluate probability calibration.
- Verify the meaning, scale, and direction of each feature.
- Develop a documented and validated risk-classification methodology.
- Improve handling of out-of-range and out-of-distribution inputs.
- Validate location-based and live-weather integrations independently.
- Expand decision-support features with appropriate, reliable data sources.

Disclaimer

FloodGuard AI is an educational machine-learning and decision-support prototype. It must not replace official weather forecasts, government alerts, emergency services, or local evacuation instructions.
