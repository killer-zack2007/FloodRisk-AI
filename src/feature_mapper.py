
"""
FloodGuard AI — Feature Mapper V2

Purpose:
    Convert validated external observations into the
    FloodGuard model's ordinal feature representation.

Important:
    Raw physical/geographic measurements must NOT be treated
    as FloodGuard scores automatically.

Every mapped feature carries:
    - FloodGuard score
    - raw value
    - unit
    - source
    - method
    - confidence
"""

from datetime import datetime, timezone


class FeatureMapper:

    FEATURES = [
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

    def __init__(self):
        self.features = {
            feature: {
                "value": None,
                "raw_value": None,
                "unit": None,
                "source": None,
                "method": None,
                "confidence": None,
                "status": "UNMAPPED"
            }
            for feature in self.FEATURES
        }

    def add_observation(
        self,
        feature,
        raw_value,
        unit=None,
        source=None,
        method=None,
        confidence="PROVISIONAL"
    ):
        """
        Add a calibrated FloodGuard feature.

        raw_value:
            Original real-world observation.

        value:
            FloodGuard 0–19 score.
            This must be supplied only after calibration.
        """

        if feature not in self.features:
            raise ValueError(
                f"Unknown FloodGuard feature: {feature}"
            )

        self.features[feature].update({
            "raw_value": raw_value,
            "unit": unit,
            "source": source,
            "method": method,
            "confidence": confidence
        })

    def set_calibrated_score(
        self,
        feature,
        score
    ):
        """
        Set validated/calibrated FloodGuard score.
        """

        if feature not in self.features:
            raise ValueError(
                f"Unknown FloodGuard feature: {feature}"
            )

        if not isinstance(score, (int, float)):
            raise TypeError(
                "FloodGuard score must be numeric."
            )

        if not 0 <= score <= 19:
            raise ValueError(
                "FloodGuard score must be between 0 and 19."
            )

        self.features[feature]["value"] = score
        self.features[feature]["status"] = "MAPPED"

    def get_mapped_features(self):
        return {
            name: data
            for name, data in self.features.items()
            if data["status"] == "MAPPED"
        }

    def get_unmapped_features(self):
        return [
            name
            for name, data in self.features.items()
            if data["status"] != "MAPPED"
        ]

    def summary(self):

        mapped = len(self.get_mapped_features())
        total = len(self.FEATURES)

        return {
            "total_features": total,
            "mapped_features": mapped,
            "unmapped_features": total - mapped,
            "coverage_percent": round(
                (mapped / total) * 100,
                2
            ),
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat()
        }

    def export(self):
        return {
            "features": self.features,
            "summary": self.summary()
        }
