
import os
import json
import joblib
import numpy as np
import pandas as pd


# ============================================================
# FLOODGUARD AI — PREDICTION ENGINE
# ============================================================

DEFAULT_FEATURE_COLUMNS = [
    "MonsoonIntensity",
    "TopographyDrainage",
    "RiverManagement",
    "Deforestation",
    "Urbanization",
    "ClimateChange",
    "DamsQuality",
    "Siltation",
    "AgriculturalPractices",
    "Encroachments",
    "IneffectiveDisasterPreparedness",
    "DrainageSystems",
    "CoastalVulnerability",
    "Landslides",
    "Watersheds",
    "DeterioratingInfrastructure",
    "PopulationScore",
    "WetlandLoss",
    "InadequatePlanning",
    "PoliticalFactors"
]


class FloodPredictor:
    """
    Core prediction engine for FloodGuard AI.

    Uses the existing trained LinearRegression model.
    """

    def __init__(self, model_path, feature_columns_path=None):

        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model file not found: {model_path}"
            )

        # Load trained model
        self.model = joblib.load(model_path)

        # ----------------------------------------------------
        # Load feature order
        # ----------------------------------------------------

        self.feature_columns = DEFAULT_FEATURE_COLUMNS.copy()

        if (
            feature_columns_path
            and os.path.exists(feature_columns_path)
        ):

            with open(feature_columns_path, "r") as file:
                loaded = json.load(file)

            if isinstance(loaded, list):
                self.feature_columns = loaded

            elif isinstance(loaded, dict):

                # Support possible JSON structures
                for key in [
                    "features",
                    "feature_columns",
                    "columns"
                ]:

                    if key in loaded:
                        self.feature_columns = loaded[key]
                        break

        # ----------------------------------------------------
        # Validate model
        # ----------------------------------------------------

        if len(self.feature_columns) != 20:

            raise ValueError(
                "FloodGuard AI expects exactly 20 features. "
                f"Found {len(self.feature_columns)}."
            )

        if hasattr(self.model, "n_features_in_"):

            if self.model.n_features_in_ != 20:

                raise ValueError(
                    "Model expects "
                    f"{self.model.n_features_in_} features, "
                    "but FloodGuard AI requires 20."
                )

    # ========================================================
    # INPUT VALIDATION
    # ========================================================

    def validate_features(self, features):

        if not isinstance(features, dict):

            raise TypeError(
                "Features must be provided as a dictionary."
            )

        missing = [
            feature
            for feature in self.feature_columns
            if feature not in features
        ]

        if missing:

            raise ValueError(
                "Missing required features: "
                + ", ".join(missing)
            )

        # Check numeric values
        for feature in self.feature_columns:

            try:
                float(features[feature])

            except (TypeError, ValueError):

                raise ValueError(
                    f"Feature '{feature}' must be numeric."
                )

    # ========================================================
    # RAW MODEL PREDICTION
    # ========================================================

    def predict(self, features):

        self.validate_features(features)

        # Preserve exact training feature order
        input_data = pd.DataFrame(
            [
                [
                    float(features[column])
                    for column in self.feature_columns
                ]
            ],
            columns=self.feature_columns
        )

        prediction = self.model.predict(input_data)[0]

        return float(prediction)

    # ========================================================
    # FLOOD RISK SCORE
    # ========================================================

    def predict_score(self, features):

        raw_prediction = self.predict(features)

        # Dataset target is on approximately 0–1 scale.
        # Convert to a project risk score of 0–100.
        score = np.clip(
            raw_prediction,
            0.0,
            1.0
        ) * 100.0

        return float(score)

    # ========================================================
    # MODEL CONTRIBUTIONS
    # ========================================================

    def get_feature_contributions(self, features):

        self.validate_features(features)

        if not hasattr(self.model, "coef_"):
            return {}

        contributions = {}

        for feature, coefficient in zip(
            self.feature_columns,
            self.model.coef_
        ):

            contributions[feature] = (
                float(features[feature]) *
                float(coefficient)
            )

        return contributions
