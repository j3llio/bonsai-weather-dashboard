from weather.fetch import get_current_conditions
from weather.rules import check_weather_rules
from weather.high_lows import daily_high_low_now


def run_weather_agent():
    # Current conditions
    conditions = get_current_conditions()
    temp = conditions["temperature_f"]
    wind = conditions["wind_mph"]

    # Daily highs/lows
    hl = daily_high_low_now(35.0456, -85.3097)
    high = hl["high_f"]
    low = hl["low_f"]

    alerts = check_weather_rules(high, wind)

    if alerts:
        print("⚠️ Weather Alerts:")
        for a in alerts:
            print(" -", a)
    else:
        print("No alerts. Conditions normal.")

