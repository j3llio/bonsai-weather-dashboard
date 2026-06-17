def check_weather_rules(temp_f, wind_mph):
    alerts = []

    if temp_f > 95:
        alerts.append(f"High heat alert: {temp_f:.1f}°F")

    if temp_f < 25:
        alerts.append(f"Freezing alert: {temp_f:.1f}°F")

    if wind_mph > 30:
        alerts.append(f"High wind alert: {wind_mph:.1f} mph")
    
    if temp_f < 45:
        alerts.append(f'Move boganvillia inside')

    return alerts
