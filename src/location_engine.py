
# ============================================================
# FLOODGUARD AI — LOCATION ENGINE
# ============================================================

from math import radians, sin, cos, sqrt, atan2


def validate_coordinates(latitude, longitude):
    """
    Validate latitude and longitude.
    """

    latitude = float(latitude)
    longitude = float(longitude)

    if not -90 <= latitude <= 90:
        raise ValueError(
            "Latitude must be between -90 and 90."
        )

    if not -180 <= longitude <= 180:
        raise ValueError(
            "Longitude must be between -180 and 180."
        )

    return latitude, longitude


def create_location(
    name,
    latitude,
    longitude
):
    """
    Create a standardized FloodGuard location object.
    """

    latitude, longitude = validate_coordinates(
        latitude,
        longitude
    )

    return {
        "name": str(name).strip() or "Selected Location",
        "latitude": latitude,
        "longitude": longitude
    }


def haversine_distance(
    latitude1,
    longitude1,
    latitude2,
    longitude2
):
    """
    Calculate approximate distance between two
    geographic coordinates in kilometres.
    """

    latitude1, longitude1 = validate_coordinates(
        latitude1,
        longitude1
    )

    latitude2, longitude2 = validate_coordinates(
        latitude2,
        longitude2
    )

    earth_radius_km = 6371.0

    lat1 = radians(latitude1)
    lat2 = radians(latitude2)

    delta_lat = radians(
        latitude2 - latitude1
    )

    delta_lon = radians(
        longitude2 - longitude1
    )

    a = (
        sin(delta_lat / 2) ** 2
        +
        cos(lat1)
        * cos(lat2)
        * sin(delta_lon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return earth_radius_km * c


def location_summary(location):
    """
    Generate a display-ready location summary.
    """

    return {
        "name": location["name"],
        "coordinates": (
            f"{location['latitude']:.6f}, "
            f"{location['longitude']:.6f}"
        )
    }
