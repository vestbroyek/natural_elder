from dotenv import load_dotenv
from geopy.geocoders import Nominatim
import os
import requests


def get_coords(location: str) -> tuple:
    geolocator = Nominatim(user_agent="natural_elder")
    location = geolocator.geocode(location)
    if location:
        return (location.latitude, location.longitude)
    else:
        return "Location not found"


def get_risk(lat: float, long: float) -> float:
    # API key
    load_dotenv()
    # call Ambee
    headers = {
        "x-api-key": os.getenv("AMBEE_API_KEY"),
        "Content-type": "application/json",
    }

    resp = requests.get(
        f"https://api.ambeedata.com/fire/v2/forecast/by-lat-lng?lat={lat}&lng={long}",
        headers=headers,
    )

    if resp.status_code == 200:
        return resp.text
    else:
        return resp.status_code
