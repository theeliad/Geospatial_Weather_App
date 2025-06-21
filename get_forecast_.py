# get_forecast_.py (CORRECTED VERSION)

import requests
import pandas as pd
import streamlit as st


# The bad import line has been removed.

@st.cache_data(ttl=600)  # Cache data for 10 minutes
def get_forecast_periods_df(latitude, longitude):
    """
    Fetches the 7-day forecast from the NWS API for a given lat/lon.
    Returns a pandas DataFrame or None if an error occurs.
    """
    # 1. First API call to get the specific forecast grid URL
    points_url = f"https://api.weather.gov/points/{latitude},{longitude}"
    headers = {"User-Agent": "Geospatial Weather App, your-email@example.com"}

    try:
        points_response = requests.get(points_url, headers=headers)
        points_response.raise_for_status()
        forecast_url = points_response.json()["properties"]["forecast"]

        # 2. Second API call to the actual forecast URL
        forecast_response = requests.get(forecast_url, headers=headers)
        forecast_response.raise_for_status()

        forecast_data = forecast_response.json()["properties"]["periods"]

        # 3. Convert the forecast data into a clean pandas DataFrame
        df = pd.DataFrame(forecast_data)

        df_display = df[
            ['name', 'startTime', 'temperature', 'temperatureUnit', 'windSpeed', 'windDirection', 'shortForecast']]
        df_display = df_display.rename(columns={
            'name': 'Period',
            'startTime': 'Time',
            'temperature': 'Temp',
            'temperatureUnit': 'Unit',
            'windSpeed': 'Wind Speed',
            'windDirection': 'Direction',
            'shortForecast': 'Forecast'
        })

        df_display['Time'] = pd.to_datetime(df_display['Time']).dt.strftime('%A, %b %d @ %I:%M %p')

        return df_display

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to retrieve weather data: {e}")
        return None
    except (KeyError, IndexError) as e:
        st.error(f"Could not parse the weather data structure: {e}")
        return None
