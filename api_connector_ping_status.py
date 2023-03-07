from nwsapy import api_connector

def api_connector_ping_status():
    """
    This function pings the NWS API to ensure that the Geospatial Weather App has access to it.
    If there is an error with the server, the function will return an error message.

    The function sets the user agent to 'Geospatial_Weather_App' and an email address to identify the source of the API request.
    It uses the ping_server() method of the api_connector object to ping the API and returns a PingResponse object that contains information about the ping request.
    If there are any request errors, the function prints an error message that includes the details of the PingResponse object.
    Otherwise, the function prints the status of the ping request, which should be "OK" if the API is accessible.
    """
    api_connector.set_user_agent('Geospatial_Weather_App', 'policapee@gmail.com')
    server_ping = api_connector.ping_server()
    if server_ping.has_any_request_errors:
        print(f"Error from server. Details: {server_ping}")
    else:
        print(server_ping.status)  # will print OK

api_connector_ping_status()
