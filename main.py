# main.py

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from get_forecast_ import get_forecast_periods_df

st.set_page_config(
    page_title="NWS Forecast Viewer",
    page_icon="🛰️",
    layout="wide"
)

@st.cache_data
def load_station_data():
    """Loads weather station data from the local CSV file."""
    try:
        df = pd.read_csv('all_weather_stations.csv')
        df['display_name'] = df['Station Name'] + " (" + df['STID'] + ")"
        return df
    except FileNotFoundError:
        st.error("Error: `all_weather_stations.csv` not found. Make sure it's in your GitHub repository.")
        return pd.DataFrame()

st.title("🛰️ NWS Weather Station Forecast")
st.markdown("Select a state and a station to view its 7-day forecast.")

all_stations_df = load_station_data()

if not all_stations_df.empty:
    st.sidebar.header("Station Selector")
    states_list = sorted(all_stations_df['State'].unique())
    selected_state = st.sidebar.selectbox("1. Select a State", states_list)
    
    stations_in_state = all_stations_df[all_stations_df['State'] == selected_state].copy()
    stations_in_state['display_name'] = stations_in_state['Station Name'] + " (" + stations_in_state['STID'] + ")"
    
    selected_station_name = st.sidebar.selectbox(
        "2. Select a Station",
        options=stations_in_state['display_name']
    )

    st.sidebar.markdown("---")
    st.sidebar.title("About")
    st.sidebar.info("""
        This app displays 7-day weather forecasts for NWS stations across the United States.
        [GitHub Repository](https://github.com/theeliad/Geospatial_Weather_App)
    """)
    st.sidebar.title("Contact")
    st.sidebar.info("""
        Eli Policape:
        [GitHub](https://github.com/theeliad) | [LinkedIn](https://www.linkedin.com/in/eli-p-96312163/)
    """)

    if selected_station_name:
        selected_station_data = stations_in_state[stations_in_state['display_name'] == selected_station_name].iloc[0]
        
        lat, lon = selected_station_data['Latitude'], selected_station_data['Longitude']
        
        st.header(f"Data for: {selected_station_data['Station Name']}")
        st.subheader(f"({selected_station_data['STID']}) - {selected_state}")

        st.markdown("**Station Location**")
        m = folium.Map(location=[lat, lon], zoom_start=10)
        folium.Marker([lat, lon], popup=selected_station_data['Station Name'], tooltip=selected_station_data['Station Name']).add_to(m)
        
        st_folium(m, height=450, width=725)

        with st.expander("View 7-Day Forecast", expanded=True):
            with st.spinner("Fetching latest forecast from NWS..."):
                forecast_df = get_forecast_periods_df(lat, lon)

            if forecast_df is not None:
                st.dataframe(forecast_df, use_container_width=True, hide_index=True)
            else:
                st.warning("Could not retrieve forecast for this location.")
    else:
        st.warning(f"No weather stations found in your CSV for the selected state: **{selected_state}**")
