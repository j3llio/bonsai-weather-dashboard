import streamlit as st
from weather.fetch import get_current_conditions
from weather.high_lows import daily_high_low_now
from weather.rules import check_weather_rules

st.set_page_config(page_title="Bonsai Weather Dashboard", page_icon="🌱")

st.title("🌱 Bonsai Weather Dashboard")

# Fetch data
conditions = get_current_conditions()
hl = daily_high_low_now(35.0456, -85.3097)

temp = conditions["temperature_f"]
wind = conditions["wind_mph"]
high = hl["high_f"]
low = hl["low_f"]

alerts = check_weather_rules(high, wind)

# Layout
col1, col2 = st.columns(2)

with col1:
    st.metric("Current Temp", f"{temp:.1f}°F")
    st.metric("Today's High", f"{high:.1f}°F")

with col2:
    st.metric("Wind Speed", f"{wind:.1f} mph")
    st.metric("Today's Low", f"{low:.1f}°F")

st.divider()

if alerts:
    st.subheader("⚠️ Alerts")
    for a in alerts:
        st.error(a)
else:
    st.success("No alerts. Conditions normal.")
