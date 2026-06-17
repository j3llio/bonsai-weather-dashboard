import requests
from datetime import datetime, timezone, date
from zoneinfo import ZoneInfo

USER_AGENT = "bonsai-weather-app (your-email@example.com)"

def get_grid_url(lat, lon):
    r = requests.get(f"https://api.weather.gov/points/{lat},{lon}",
                     headers={"User-Agent": USER_AGENT}, timeout=10)
    r.raise_for_status()
    return r.json()["properties"]["forecastGridData"]

def fetch_temperature_values(grid_url):
    r = requests.get(grid_url, headers={"User-Agent": USER_AGENT}, timeout=10)
    r.raise_for_status()
    props = r.json().get("properties", {})
    return props.get("temperature", {}).get("values", [])

def iso_to_aware_dt(iso_str):
    start = iso_str.split("/")[0]
    return datetime.fromisoformat(start)

def c_to_f(c):
    return c * 9/5 + 32

def daily_high_low_now(lat, lon, tz_name="America/New_York"):
    grid_url = get_grid_url(lat, lon)
    temps = fetch_temperature_values(grid_url)

    tz = ZoneInfo(tz_name)
    rows = []

    for v in temps:
        val = v.get("value")
        if val is None:
            continue

        dt_utc = iso_to_aware_dt(v["validTime"])
        if dt_utc.tzinfo is None:
            dt_utc = dt_utc.replace(tzinfo=timezone.utc)

        local_dt = dt_utc.astimezone(tz)
        rows.append((local_dt.date(), c_to_f(val)))

    today = date.today()
    today_vals = [t for d, t in rows if d == today]

    if not today_vals:
        return None

    return {
        "date": today,
        "high_f": round(max(today_vals), 1),
        "low_f": round(min(today_vals), 1)
    }
