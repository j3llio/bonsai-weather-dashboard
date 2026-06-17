import requests
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

USER_AGENT = "bonsai-weather-app (your-email@example.com)"

def get_current_conditions():
    url = "https://api.weather.gov/gridpoints/MRX/65,55"
    headers = {"User-Agent": USER_AGENT}

    response = requests.get(url, headers=headers)
    data = response.json()

    temp = data["properties"]["temperature"]["values"][0]["value"]
    wind = data["properties"]["windSpeed"]["values"][0]["value"]

    temp_f = (temp * 9/5) + 32

    return {"temperature_f": temp_f, "wind_mph": wind}
