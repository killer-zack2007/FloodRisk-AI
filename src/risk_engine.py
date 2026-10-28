
# ============================================================
# FLOODGUARD AI — RISK ENGINE
# ============================================================


def classify_risk(score):
    """
    Convert the FloodGuard AI risk score into
    an application-defined risk category.
    """

    score = float(score)

    if score < 25:
        return "LOW"

    elif score < 50:
        return "MODERATE"

    elif score < 75:
        return "HIGH"

    else:
        return "VERY HIGH"


def get_risk_emoji(level):

    return {
        "LOW": "🟢",
        "MODERATE": "🟡",
        "HIGH": "🟠",
        "VERY HIGH": "🔴"
    }.get(level, "⚪")


def get_risk_description(level):

    descriptions = {

        "LOW":
            "The model assessment indicates relatively "
            "lower flood risk.",

        "MODERATE":
            "The model assessment indicates moderate "
            "flood risk. Continue monitoring relevant "
            "conditions.",

        "HIGH":
            "The model assessment indicates elevated "
            "flood risk. Additional preparedness and "
            "monitoring are recommended.",

        "VERY HIGH":
            "The model assessment indicates very high "
            "flood risk. Follow relevant official "
            "warnings and emergency guidance."
    }

    return descriptions.get(
        level,
        "Risk level unavailable."
    )


def build_risk_result(score):

    score = float(score)

    level = classify_risk(score)

    return {
        "score": round(score, 2),
        "level": level,
        "emoji": get_risk_emoji(level),
        "description": get_risk_description(level)
    }
