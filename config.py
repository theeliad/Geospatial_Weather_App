import os

stations_url = 'https://forecast.weather.gov/stations.php'
### In the future API keys and User Account Information can be stored here. ###
filepath = os.getcwd()
filename = "all_weather_stations.csv"
filepath_filename = os.path.join(filepath, filename)