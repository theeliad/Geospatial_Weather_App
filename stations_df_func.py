import pandas as pd

stations_url = 'https://forecast.weather.gov/stations.php'


def get_stations_df(stations_url):
    """
    Reads an HTML table from the given URL using the `read_html` function of Pandas,
    drops missing values from the table, saves it as a CSV file, drops the index column,
    and returns the resulting DataFrame.

    Args:
        stations_url (str): The URL of the webpage containing the weather stations data.

    Returns:
        pandas.DataFrame: A DataFrame of weather stations without the index column.
    """

    try:
        stations_df = pd.read_html(stations_url, header=0)
        stations_df = stations_df[4]
        stations_df = stations_df.dropna()
        stations_df = stations_df.reset_index(drop=True)
        stations_df.to_csv("all_weather_stations.csv")
        return stations_df
    except Exception as e:
        print(f"An error occurred while processing the stations data: {e}")


get_stations_df(stations_url)



# Get the DataFrame of weather stations
#def get_stations():
#    stations_df = get_stations_df(stations_url)
#    return stations_df

#stations_df = get_stations()