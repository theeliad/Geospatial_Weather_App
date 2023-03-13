import pandas as pd
from nwsapy import api_connector


def get_forecast_periods_df(output):
    """
    Obtains weather forecast data from a given latitude and longitude using an API connector module.

    Parameters:
    output (dict): A dictionary containing the latitude and longitude of the location for which to retrieve weather forecast data.

    Returns:
    pandas.DataFrame: A dataframe containing weather forecast data for the specified location.
    """

    # Sets the user agent to 'Geospatial_Weather_App' and an email address to identify the source of the API request.
    api_connector.set_user_agent('Geospatial_Weather_App', 'null')

    # Obtain latitude and longitude data for a given location using the api_connector module
    latlon_pointdata = api_connector.get_point(output['last_object_clicked']['lat'],
                                               output['last_object_clicked']['lng'])
    latlon_pointdata_dict = latlon_pointdata.to_dict()

    # Make a request to a weather API using the obtained data and convert the resulting data from JSON to a Pandas dataframe
    full_forecast = api_connector.make_request(latlon_pointdata_dict['forecast'])
    full_forecast_json = full_forecast.json()
    full_forecast_df = pd.json_normalize(full_forecast_json)

    # Extract relevant weather forecast data from the dataframe and drop unnecessary columns
    full_forecast_properties_periods_list = full_forecast_df['properties.periods'][0]
    full_forecast_periods_df = pd.DataFrame.from_records(full_forecast_properties_periods_list)
    full_forecast_periods_df = full_forecast_periods_df.drop(columns=['number', 'temperatureTrend',
                                                                      'probabilityOfPrecipitation',
                                                                      'dewpoint', 'relativeHumidity', 'icon'])
    # Return the resulting dataframe
    return full_forecast_periods_df


if __name__ == "__main__":
    output = {'last_object_clicked': {'lat': 39.9, 'lng': -99.9}}
    detailed_forecast_df = get_forecast_periods_df(output)
    print(detailed_forecast_df)
