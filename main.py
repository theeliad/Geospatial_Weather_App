import folium
import numpy as np
import streamlit as st
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

from get_forecast import get_forecast_periods_df
from stations_df_func import get_stations_df, stations_url


st.set_page_config(layout="wide")


@st.cache_resource(show_spinner=False)
def get_stations():
    stations_df = get_stations_df(stations_url)
    return stations_df


@st.cache_resource(show_spinner=False)
def get_marker_cluster(data):
    '''Add markers with popups and clustering'''
    marker_cluster = MarkerCluster()
    for i in range(len(data)):
        folium.Marker(
            location=[data.iloc[i]["Latitude"], data.iloc[i]["Longitude"]],
            popup=f"Name: {data.iloc[i]['Station Name']}, STID: {data.iloc[i]['STID']}, State: {data.iloc[i]['State']}",
        ).add_to(marker_cluster)
    return marker_cluster


@st.cache_resource(show_spinner=False)
def get_folium_map(stations_df):
    '''Create a folium map with a marker cluster'''
    location = [np.mean(stations_df.Latitude), np.mean(stations_df.Longitude)]
    folium_map = folium.Map(
        location=location,
        tiles='OpenStreetMap',
        zoom_start=5
    )
    marker_cluster = get_marker_cluster(stations_df)
    marker_cluster.add_to(folium_map)
    folium.LayerControl().add_to(folium_map)
    folium.plugins.LocateControl().add_to(folium_map)
    folium.plugins.Fullscreen().add_to(folium_map)
    folium.plugins.Geocoder().add_to(folium_map)
    return folium_map


@st.cache_data(show_spinner=False)
def get_forecast_df(output):
    '''Get the forecast data from the NWS API'''
    forecast_df = get_forecast_periods_df(output)
    return forecast_df


def main():
    '''Shows the title and sidebar of the app
    '''
    st.title("Geospatial Weather App")
    st.sidebar.title("About")
    st.sidebar.info(
        """
        GitHub repository: <https://github.com/theeliad>
        """
    )
    st.sidebar.title("Contact")
    st.sidebar.info(
        """
        Eli Policape:
        [GitHub](https://github.com/theeliad) | [LinkedIn](https://www.linkedin.com/in/eli-p-96312163/)
        """
    )


def app():
    """
        A Streamlit app that displays a map of weather stations in the United States using data from the National Weather Service API.
        Processes it using Pandas, and displays it as a table and a map using Folium.
        The map shows the locations of the weather stations, and includes controls for clustering, location search, and full-screen display.
        The app also uses the Streamlit-Folium integration to display the map in a Streamlit component.
    """

    st.header("Search Weather Maps")
    st.markdown(
        """
    This Streamlit app displays of map of weather stations in the United States using weather data from the National Weather Service API in just a few clicks.

        """
    )

    col1, col2 = st.columns([3, 1])
    width = 1000
    height = 600

    with col2:
        with st.spinner("Loading weather stations..."):
            # Get the DataFrame of weather stations
            stations_df = get_stations()
        # Display the DataFrame of weather stations
        st.dataframe(stations_df)

    with col1:
        # Display the Map of weather stations
        folium_map = get_folium_map(stations_df)
        # Save last object clicked to session state
        # if "last_object_clicked" not in st.session_state:
        #     st.session_state["last_object_clicked"] = None

        # # Load last object clicked if it exists
        # last_object_clicked = st.session_state["last_object_clicked"]

        # Display the map
        output = st_folium(
            folium_map, width=width, height=height, returned_objects=["last_object_clicked"]
        )

    # with col2:
    #     st.write(output)

    st.header("Weather Forecast")
    if output["last_object_clicked"] is not None:
        st.write(f"Forecast for Latitude: {output['last_object_clicked']['lat']} Longitude: {output['last_object_clicked']['lng']}")
        with st.spinner("Loading weather forecast..."):
            detailed_forecast_df = get_forecast_df(output)
            st.dataframe(detailed_forecast_df)


if __name__ == "__main__":
    main()
    app()
