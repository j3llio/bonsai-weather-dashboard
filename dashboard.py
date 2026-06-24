import streamlit as st
import pandas as pd
from weather.fetch import get_current_conditions
from weather.high_lows import daily_high_low_now, daily_max_wind_now
from weather.rules import check_weather_rules
from visuals import create_bonsai_chart

st.set_page_config(page_title="Bonsai Weather Dashboard", page_icon="🌱", layout="wide")

st.title("🌱 Bonsai Weather Dashboard")

# --- Load tree data ---
import os
df = pd.read_csv(os.path.join(os.path.dirname(__file__), "Data", "Tree_data.csv"))

# --- Sidebar ---
with st.sidebar:

    # -- Weather --
    st.subheader("☁️ Weather")

    conditions = get_current_conditions()
    hl = daily_high_low_now(35.0456, -85.3097)
    max_wind = daily_max_wind_now(35.0456, -85.3097)

    temp = conditions["temperature_f"]
    wind = conditions["wind_mph"]
    high = hl["high_f"]
    low = hl["low_f"]

    alerts = check_weather_rules(high, wind)

    col1, col2 = st.columns(2)
    col1.metric("Temp", f"{temp:.1f}°F")
    col1.metric("High", f"{high:.1f}°F")
    col2.metric("Wind", f"{wind:.1f} mph")
    col2.metric("Low", f"{low:.1f}°F")

    st.metric("Max Wind (forecast)", f"{max_wind:.1f} mph" if max_wind is not None else "N/A")

    if alerts:
        st.divider()
        st.subheader("⚠️ Alerts")
        for a in alerts:
            st.error(a)
    else:
        st.success("✅ Conditions normal.")

    st.divider()

    # -- Tree list --
    st.subheader("🌳 Your Trees")

    for _, row in df.iterrows():
        with st.expander(row["Tree"]):
            st.write(f"☀️ **Sun needs:** {row['Sun']} hrs/day")
            st.write(f"💧 **Water needs:** {row['Water']} / 10")
            st.write(f"💨 **Wind tolerance:** {row['Wind']} / 10")
            st.write(f"📈 **Growth rate:** {row['Growth']} / 10")

# --- Main area: chart ---
st.subheader("📊 Placement & Care Guide")
fig = create_bonsai_chart(df)
st.pyplot(fig, use_container_width=True)
