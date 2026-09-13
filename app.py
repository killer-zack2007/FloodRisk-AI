
import os
import json
import joblib
import numpy as np
import pandas as pd
import streamlit as st


# ============================================================
# CONFIG
# ============================================================



# ============================================================
# MODEL PATHS — WORKS IN COLAB + STREAMLIT CLOUD
# ============================================================

from pathlib import Path

# Folder containing app.py
BASE_DIR = Path(__file__).resolve().parent

# Deployment paths — used by Streamlit Cloud / GitHub
LOCAL_MODEL_PATH = BASE_DIR / "models" / "flood_prediction_model.joblib"
LOCAL_FEATURE_PATH = BASE_DIR / "models" / "feature_columns.json"
LOCAL_METADATA_PATH = BASE_DIR / "models" / "model_metadata.json"

# Colab Google Drive fallback
DRIVE_ROOT = Path("/content/drive/MyDrive/Flood_Prediction")
DRIVE_MODEL_PATH = DRIVE_ROOT / "models" / "flood_prediction_model.joblib"
DRIVE_FEATURE_PATH = DRIVE_ROOT / "models" / "feature_columns.json"
DRIVE_METADATA_PATH = DRIVE_ROOT / "models" / "model_metadata.json"

# Automatically select the correct location
MODEL_PATH = (
    LOCAL_MODEL_PATH
    if LOCAL_MODEL_PATH.exists()
    else DRIVE_MODEL_PATH
)

FEATURE_PATH = (
    LOCAL_FEATURE_PATH
    if LOCAL_FEATURE_PATH.exists()
    else DRIVE_FEATURE_PATH
)

METADATA_PATH = (
    LOCAL_METADATA_PATH
    if LOCAL_METADATA_PATH.exists()
    else DRIVE_METADATA_PATH
)

# Safety check
if not MODEL_PATH.exists():
    raise FileNotFoundError(
        "Flood prediction model not found. "
        "Expected it in the project's models/ folder."
    )

if not FEATURE_PATH.exists():
    raise FileNotFoundError(
        "Feature list not found. "
        "Expected feature_columns.json in models/."
    )

MODEL_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "flood_prediction_model.joblib"
)

FEATURE_PATH = os.path.join(
    PROJECT_ROOT,
    "models",
    "feature_columns.json"
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="FloodRisk AI",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# PREMIUM UI
# ============================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background:
        radial-gradient(circle at 10% 10%, rgba(0, 212, 255, 0.08), transparent 28%),
        radial-gradient(circle at 90% 15%, rgba(139, 92, 246, 0.10), transparent 30%),
        #070910;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* Main title */

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(2.4rem, 6vw, 4.8rem);
    font-weight: 800;
    letter-spacing: -3px;
    margin: 0;
    line-height: 1;
    background: linear-gradient(90deg, #ffffff, #8be9ff, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-subtitle {
    color: #9ca3af;
    font-size: 1rem;
    margin-top: 12px;
    max-width: 650px;
}

.badge {
    display: inline-block;
    padding: 7px 13px;
    border: 1px solid rgba(255,255,255,0.12);
    border-radius: 999px;
    background: rgba(255,255,255,0.04);
    color: #b9eaff;
    font-size: 0.78rem;
    font-weight: 600;
    margin-bottom: 15px;
}

/* Cards */

.glass-card {
    background: rgba(17, 24, 39, 0.68);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 22px;
    padding: 24px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.22);
    backdrop-filter: blur(18px);
}

.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #f9fafb;
    margin-bottom: 4px;
}

.section-subtitle {
    color: #8b93a7;
    font-size: 0.85rem;
    margin-bottom: 18px;
}

/* Risk score */

.risk-score {
    text-align: center;
    padding: 35px 20px;
}

.risk-number {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(3.2rem, 8vw, 5.8rem);
    font-weight: 800;
    line-height: 1;
    color: #ffffff;
}

.risk-label {
    display: inline-block;
    margin-top: 15px;
    padding: 8px 18px;
    border-radius: 999px;
    background: rgba(255,255,255,0.08);
    color: #dbeafe;
    font-weight: 700;
    letter-spacing: 0.5px;
}

/* Stats */

.stat-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: white;
}

.stat-label {
    color: #8b93a7;
    font-size: 0.78rem;
    margin-top: 4px;
}

/* Factor bars */

.factor-row {
    margin: 12px 0;
}

.factor-name {
    display: flex;
    justify-content: space-between;
    color: #d1d5db;
    font-size: 0.82rem;
    margin-bottom: 6px;
}

.factor-bar-bg {
    height: 8px;
    background: rgba(255,255,255,0.07);
    border-radius: 99px;
    overflow: hidden;
}

.factor-bar {
    height: 100%;
    border-radius: 99px;
    background: linear-gradient(90deg, #06b6d4, #8b5cf6);
}

/* Insight */

.insight {
    border-left: 3px solid #22d3ee;
    padding: 12px 15px;
    margin: 10px 0;
    background: rgba(34,211,238,0.05);
    border-radius: 0 12px 12px 0;
    color: #cbd5e1;
    font-size: 0.88rem;
}

/* Buttons */

.stButton > button {
    width: 100%;
    border-radius: 13px;
    min-height: 48px;
    font-weight: 700;
    border: 1px solid rgba(255,255,255,0.10);
}

/* Inputs */

div[data-testid="stNumberInput"] {
    margin-bottom: 5px;
}

div[data-testid="stNumberInput"] label {
    color: #b8c0d0 !important;
    font-size: 0.78rem !important;
}

/* Divider */

hr {
    border-color: rgba(255,255,255,0.08) !important;
}

/* Footer */

.footer {
    text-align: center;
    color: #667085;
    font-size: 0.75rem;
    padding: 35px 0 10px;
}

@media (max-width: 700px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .hero-title {
        letter-spacing: -2px;
    }

    .glass-card {
        padding: 18px;
        border-radius: 17px;
    }
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# MODEL LOADING
# ============================================================

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)


@st.cache_data
def load_features():
    with open(FEATURE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


model = load_model()
FEATURES = load_features()


# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "prediction" not in st.session_state:
    st.session_state.prediction = None


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="badge">AI-POWERED FLOOD RISK ANALYSIS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-title">🌊 FloodRisk AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-subtitle">'
    'Estimate flood probability, understand the strongest risk factors, '
    'and explore how changing conditions may affect the model prediction.'
    '</div>',
    unsafe_allow_html=True
)

st.write("")


# ============================================================
# MODEL STATS
# ============================================================

cols = st.columns(4)

stats = [
    ("1.12M+", "Training Records"),
    ("20", "Risk Factors"),
    ("84.49%", "Validation R²"),
    ("0.01579", "Validation MAE"),
]

for col, (value, label) in zip(cols, stats):
    with col:
        st.markdown(
            f"""
            <div class="glass-card">
                <div class="stat-value">{value}</div>
                <div class="stat-label">{label}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


st.write("")


# ============================================================
# EXAMPLE SCENARIOS
# ============================================================

st.markdown(
    '<div class="section-title">⚡ Quick Start</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Load a ready-made scenario or enter your own values below.'
    '</div>',
    unsafe_allow_html=True
)

scenario_cols = st.columns(3)

scenario_values = {
    "🌱 Low Risk Demo": [2] * 20,
    "🏙️ Urban Risk Demo": [8] * 20,
    "🌧️ High Risk Demo": [14] * 20,
}

selected_scenario = None

with scenario_cols[0]:
    if st.button("🌱 Low Risk Demo"):
        selected_scenario = scenario_values["🌱 Low Risk Demo"]

with scenario_cols[1]:
    if st.button("🏙️ Urban Risk Demo"):
        selected_scenario = scenario_values["🏙️ Urban Risk Demo"]

with scenario_cols[2]:
    if st.button("🌧️ High Risk Demo"):
        selected_scenario = scenario_values["🌧️ High Risk Demo"]


if selected_scenario is not None:
    for feature, value in zip(FEATURES, selected_scenario):
        st.session_state[f"input_{feature}"] = value

    st.rerun()


# ============================================================
# INPUT CATEGORIES
# ============================================================

categories = {
    "🌧️ Environmental Conditions": [
        "MonsoonIntensity",
        "ClimateChange",
        "Landslides",
        "Watersheds",
        "WetlandLoss",
    ],

    "🏙️ Urban & Infrastructure": [
        "Urbanization",
        "DrainageSystems",
        "DeterioratingInfrastructure",
        "InadequatePlanning",
        "TopographyDrainage",
    ],

    "🌳 Human Impact": [
        "Deforestation",
        "AgriculturalPractices",
        "Encroachments",
        "PopulationScore",
    ],

    "🌊 Water Management": [
        "RiverManagement",
        "DamsQuality",
        "Siltation",
    ],

    "🏛️ Governance & Vulnerability": [
        "IneffectiveDisasterPreparedness",
        "CoastalVulnerability",
        "PoliticalFactors",
    ],
}


st.markdown("---")

st.markdown(
    '<div class="section-title">🎛️ Risk Factor Configuration</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="section-subtitle">'
    'Dataset scale: values from 0 to 19. Higher values represent stronger '
    'presence of the corresponding factor in the model input.'
    '</div>',
    unsafe_allow_html=True
)


values = {}

for category, feature_list in categories.items():

    with st.expander(category, expanded=True):

        cols = st.columns(2)

        for i, feature in enumerate(feature_list):

            default_value = st.session_state.get(
                f"input_{feature}",
                5
            )

            with cols[i % 2]:

                values[feature] = st.number_input(
                    feature,
                    min_value=0,
                    max_value=19,
                    value=int(default_value),
                    step=1,
                    key=f"input_{feature}"
                )


# ============================================================
# PREDICT
# ============================================================

st.write("")

predict_clicked = st.button(
    "🌊  ANALYZE FLOOD RISK",
    type="primary",
    use_container_width=True
)


if predict_clicked:

    input_df = pd.DataFrame(
        [[values[f] for f in FEATURES]],
        columns=FEATURES
    )

    prediction = float(model.predict(input_df)[0])

    prediction = float(np.clip(prediction, 0.0, 1.0))

    st.session_state.prediction = prediction

    st.session_state.history.append({
        "Prediction": prediction,
        "Time": pd.Timestamp.now().strftime("%H:%M:%S")
    })

    # Keep last 10
    st.session_state.history = st.session_state.history[-10:]


# ============================================================
# RESULT
# ============================================================

if st.session_state.prediction is not None:

    prediction = st.session_state.prediction
    percentage = prediction * 100

    if percentage < 35:
        risk = "LOW"
    elif percentage < 55:
        risk = "MODERATE"
    elif percentage < 70:
        risk = "HIGH"
    else:
        risk = "VERY HIGH"

    st.write("")
    st.markdown("---")
    st.write("")

    # --------------------------------------------------------
    # SCORE
    # --------------------------------------------------------

    st.markdown(
        f"""
        <div class="glass-card risk-score">
            <div class="section-subtitle">CURRENT FLOOD RISK SCORE</div>
            <div class="risk-number">{percentage:.1f}%</div>
            <div class="risk-label">⚠️ {risk} RISK</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    # --------------------------------------------------------
    # SCORE METRICS
    # --------------------------------------------------------

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Probability",
            f"{prediction:.4f}"
        )

    with c2:
        st.metric(
            "Percentage",
            f"{percentage:.2f}%"
        )

    with c3:
        st.metric(
            "Risk Level",
            risk
        )


    # ========================================================
    # EXPLAINABLE AI
    # ========================================================

    st.write("")
    st.markdown("---")
    st.write("")

    st.markdown(
        '<div class="section-title">🧠 Why did the model predict this?</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'These are the strongest positive contributions to the current prediction, '
        'based on the trained Linear Regression model.'
        '</div>',
        unsafe_allow_html=True
    )

    coefficients = np.asarray(model.coef_).reshape(-1)

    contributions = []

    for feature, value, coefficient in zip(
        FEATURES,
        [values[f] for f in FEATURES],
        coefficients
    ):
        contribution = float(value * coefficient)

        contributions.append({
            "feature": feature,
            "value": value,
            "contribution": contribution
        })

    contribution_df = pd.DataFrame(contributions)

    top_positive = contribution_df.sort_values(
        "contribution",
        ascending=False
    ).head(6)

    max_contribution = max(
        abs(top_positive["contribution"]).max(),
        0.000001
    )

    for _, row in top_positive.iterrows():

        strength = min(
            100,
            abs(row["contribution"]) / max_contribution * 100
        )

        st.markdown(
            f"""
            <div class="factor-row">
                <div class="factor-name">
                    <span>{row["feature"]}</span>
                    <span>+{row["contribution"]:.4f}</span>
                </div>
                <div class="factor-bar-bg">
                    <div class="factor-bar"
                         style="width:{strength:.1f}%">
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # AI INSIGHTS
    # ========================================================

    strongest = top_positive.iloc[0]["feature"]

    second = (
        top_positive.iloc[1]["feature"]
        if len(top_positive) > 1
        else strongest
    )

    st.write("")

    st.markdown(
        '<div class="section-title">💡 Risk Insights</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="insight">
        🔎 <b>Strongest model contribution:</b> {strongest}
        </div>

        <div class="insight">
        📊 <b>Another influential factor:</b> {second}
        </div>

        <div class="insight">
        🎯 The current model estimate is based on all 20 supplied risk factors.
        </div>

        <div class="insight">
        ⚠️ This is a machine-learning estimate, not an official emergency,
        weather, or government flood warning.
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # WHAT-IF SIMULATOR
    # ========================================================

    st.write("")
    st.markdown("---")
    st.write("")

    st.markdown(
        '<div class="section-title">⚡ What-If Scenario Simulator</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="section-subtitle">'
        'Explore how changing one factor affects the model output. '
        'This is a mathematical model scenario, not a real-world guarantee.'
        '</div>',
        unsafe_allow_html=True
    )

    scenario_feature = st.selectbox(
        "Choose a factor",
        FEATURES,
        key="scenario_feature"
    )

    current_value = values[scenario_feature]

    scenario_value = st.slider(
        f"Change {scenario_feature}",
        min_value=0,
        max_value=19,
        value=current_value,
        key="scenario_value"
    )

    scenario_values_dict = values.copy()
    scenario_values_dict[scenario_feature] = scenario_value

    scenario_df = pd.DataFrame(
        [[scenario_values_dict[f] for f in FEATURES]],
        columns=FEATURES
    )

    scenario_prediction = float(
        model.predict(scenario_df)[0]
    )

    scenario_prediction = float(
        np.clip(scenario_prediction, 0.0, 1.0)
    )

    change = (scenario_prediction - prediction) * 100

    w1, w2, w3 = st.columns(3)

    with w1:
        st.metric(
            "Current",
            f"{prediction * 100:.2f}%"
        )

    with w2:
        st.metric(
            "Scenario",
            f"{scenario_prediction * 100:.2f}%"
        )

    with w3:
        st.metric(
            "Change",
            f"{change:+.2f}%"
        )


    # ========================================================
    # PREDICTION HISTORY
    # ========================================================

    if len(st.session_state.history) > 1:

        st.write("")
        st.markdown("---")
        st.write("")

        st.markdown(
            '<div class="section-title">📈 Prediction History</div>',
            unsafe_allow_html=True
        )

        history_df = pd.DataFrame(
            st.session_state.history
        )

        history_df["Probability (%)"] = (
            history_df["Prediction"] * 100
        )

        st.line_chart(
            history_df.set_index("Time")["Probability (%)"]
        )


# ============================================================
# MODEL INFORMATION
# ============================================================

st.write("")
st.markdown("---")
st.write("")

with st.expander("🔬 Model Information"):

    st.markdown(
        """
        **Algorithm:** Linear Regression

        **Validation R²:** 0.8449

        **Validation MAE:** 0.01579

        **Validation RMSE:** 0.02008

        **Training records:** 1,117,957

        **Input features:** 20

        The final model was selected after benchmarking multiple
        approaches. Linear Regression achieved the strongest validation
        performance among the tested models and also provides interpretable
        feature coefficients.
        """
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🌊 FloodRisk AI · Machine Learning Flood Probability Estimator
        <br>
        Built with Python · Scikit-learn · Streamlit
    </div>
    """,
    unsafe_allow_html=True
)