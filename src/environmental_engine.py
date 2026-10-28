
import requests
from datetime import datetime


class EnvironmentalEngine:
    """
    FloodGuard AI Environmental Data Engine.

    V1 collects location-specific weather/environmental data.
    It does NOT convert the data into ML features.
    """

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, timeout=15):
        self.timeout = timeout

    def get_environmental_data(self, latitude, longitude):

        if not (-90 <= latitude <= 90):
            raise ValueError(
                "Latitude must be between -90 and 90."
            )

        if not (-180 <= longitude <= 180):
            raise ValueError(
                "Longitude must be between -180 and 180."
            )

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,"
                "relative_humidity_2m,"
                "precipitation,"
                "rain,"
                "pressure_msl,"
                "wind_speed_10m"
            ),
            "hourly": (
                "precipitation,"
                "rain,"
                "temperature_2m"
            ),
            "forecast_days": 3,
            "timezone": "auto"
        }

        try:
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=self.timeout
            )

            response.raise_for_status()

            data = response.json()

        except requests.RequestException as e:
            raise RuntimeError(
                f"Environmental data request failed: {e}"
            )

        current = data.get("current", {})
        hourly = data.get("hourly", {})

        return {
            "source": "Open-Meteo",

            "retrieved_at": datetime.utcnow().isoformat(),

            "location": {
                "latitude": latitude,
                "longitude": longitude
            },

            "current": {
                "temperature_c": current.get(
                    "temperature_2m"
                ),

                "relative_humidity_percent": current.get(
                    "relative_humidity_2m"
                ),

                "precipitation_mm": current.get(
                    "precipitation"
                ),

                "rain_mm": current.get(
                    "rain"
                ),

                "pressure_msl_hpa": current.get(
                    "pressure_msl"
                ),

                "wind_speed_kmh": current.get(
                    "wind_speed_10m"
                )
            },

            "forecast": {
                "time": hourly.get(
                    "time",
                    []
                ),

                "precipitation_mm": hourly.get(
                    "precipitation",
                    []
                ),

                "rain_mm": hourly.get(
                    "rain",
                    []
                ),

                "temperature_c": hourly.get(
                    "temperature_2m",
                    []
                )
            }
        }
