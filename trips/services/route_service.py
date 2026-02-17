import requests
import polyline
from django.conf import settings


class RouteService:

    DIRECTIONS_URL = "https://api.openrouteservice.org/v2/directions/driving-car"
    GEOCODE_URL = "https://api.openrouteservice.org/geocode/search"

    @staticmethod
    def geocode(location: str):
        headers = {"Authorization": settings.ORS_API_KEY}
        params = {"text": location, "size": 1}

        response = requests.get(
            RouteService.GEOCODE_URL,
            headers=headers,
            params=params,
            timeout=30
        )

        if response.status_code != 200:
            raise Exception(f"Geocode Error: {response.text}")

        data = response.json()

        if not data.get("features"):
            raise Exception(f"Location not found: {location}")

        return data["features"][0]["geometry"]["coordinates"]

    @classmethod
    def get_route(cls, start, pickup, dropoff):

        headers = {
            "Authorization": settings.ORS_API_KEY,
            "Content-Type": "application/json",
        }

        body = {
            "coordinates": [start, pickup, dropoff],
            "instructions": True
        }

        response = requests.post(
            cls.DIRECTIONS_URL,
            json=body,
            headers=headers,
            timeout=30
        )

        if response.status_code != 200:
            raise Exception(f"Route Error: {response.text}")

        data = response.json()

        route = data["routes"][0]
        summary = route["summary"]

        encoded_geometry = route["geometry"]
        decoded = polyline.decode(encoded_geometry)
        geometry = [[lat, lng] for lat, lng in decoded]

        steps = []
        for segment in route.get("segments", []):
            steps.extend(segment.get("steps", []))

        return {
            "distance_miles": round(summary["distance"] / 1609.34, 2),
            "duration_hours": round(summary["duration"] / 3600, 2),
            "geometry": geometry,
            "steps": steps,
        }
