import streamlit as st
import numpy as np
#from config import stations_url
from get_forecast import get_forecast_periods_df
from stations_df_func import get_stations_df, stations_url
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import folium
# stations_url = 'https://forecast.weather.gov/stations.php'

st.set_page_config(layout="wide")


def main():

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

    st.title("Search Weather Maps")
    st.markdown(
        """
    This Streamlit app displays of map of weather stations in the United States using weather data from the National Weather Service API in just a few clicks.
    
        """
    )

    row1_col1, row1_col2 = st.columns([3, 1])
    width = 1000
    height = 600
    tiles = None

    with row1_col2:
        # Get the DataFrame of weather stations

        @st.cache_resource
        def get_stations():
            stations_df = get_stations_df(stations_url)
            return stations_df

        stations_df = get_stations()

        # Display the DataFrame of weather stations
        #st.dataframe(stations_df)

        with row1_col1:
            # Display the Map of weather stations

            data = stations_df
            location = [np.mean(data.Latitude), np.mean(data.Longitude)]
            t = folium.Map(
                location=location,
                tiles='OpenStreetMap',
                zoom_start=5
            )

            # Add markers with popups and clustering
            @st.cache_data
            def get_marker_cluster(data):
                marker_cluster = MarkerCluster()
                for i in range(len(data)):
                    folium.Marker(
                        location=[data.iloc[i]["Latitude"], data.iloc[i]["Longitude"]],
                        popup=f"Name: {data.iloc[i]['Station Name']}, STID: {data.iloc[i]['STID']}, State: {data.iloc[i]['State']}",
                    ).add_to(marker_cluster)
                return marker_cluster
            marker_cluster = get_marker_cluster(data)
            marker_cluster.add_to(t)

            folium.LayerControl().add_to(t)
            folium.plugins.LocateControl().add_to(t)
            folium.plugins.Fullscreen().add_to(t)
            folium.plugins.Geocoder().add_to(t)

            # Save last object clicked to session state
            if "last_object_clicked" not in st.session_state:
                st.session_state["last_object_clicked"] = None

            # Load last object clicked if it exists
            last_object_clicked = st.session_state["last_object_clicked"]

            output = st_folium(
                t, width=width, height=height, returned_objects=["last_object_clicked"]
            )

    with row1_col2:
        st.write(output)
        st.write(type(marker_cluster))
    with st.expander("Click here to expand and view weather forecast"):
        if output["last_object_clicked"] is not None:
            detailed_forecast_df = get_forecast_periods_df(output)
            st.dataframe(detailed_forecast_df)
main()
app()
