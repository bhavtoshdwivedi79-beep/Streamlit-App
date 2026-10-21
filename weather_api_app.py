
import streamlit as st
import requests

st.set_page_config(page_title="Weather App", page_icon="🌦️")

st.title("🌦️ Current Weather App")
st.write("Find the current temperature of any city.")

city = st.text_input("Enter city name")

if st.button("Get Weather"):
    if city.strip():
        try:
            # Find city coordinates
            geo_url = "https://geocoding-api.open-meteo.com/v1/search"
            geo_response = requests.get(
                geo_url,
                params={"name": city, "count": 1},
                timeout=15
            )
            geo_response.raise_for_status()
            locations = geo_response.json().get("results", [])

            if not locations:
                st.error("City not found. Please try again.")
            else:
                place = locations[0]
                latitude = place["latitude"]
                longitude = place["longitude"]

                # Get current weather
                weather_url = "https://api.open-meteo.com/v1/forecast"
                weather_response = requests.get(
                    weather_url,
                    params={
                        "latitude": latitude,
                        "longitude": longitude,
                        "current": (
                            "temperature_2m,relative_humidity_2m,"
                            "apparent_temperature,wind_speed_10m,weather_code"
                        ),
                        "timezone": "auto"
                    },
                    timeout=15
                )
                weather_response.raise_for_status()
                current = weather_response.json()["current"]

                st.subheader(
                    f"{place['name']}, {place.get('country', '')}"
                )

                st.metric(
                    "Current Temperature",
                    f"{current['temperature_2m']} °C"
                )
                st.metric(
                    "Feels Like",
                    f"{current['apparent_temperature']} °C"
                )
                st.metric(
                    "Humidity",
                    f"{current['relative_humidity_2m']}%"
                )
                st.metric(
                    "Wind Speed",
                    f"{current['wind_speed_10m']} km/h"
                )
                st.write(
                    "Weather Code:",
                    current["weather_code"]
                )
                st.caption("Weather data: Open-Meteo")

        except requests.RequestException:
            st.error(
                "Unable to fetch weather. Check your internet connection."
            )
    else:
        st.warning("Please enter a city name.")
