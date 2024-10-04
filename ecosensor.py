import httpx
import aws

AWS_CF_URL = "https://d17kn6fj50jzfv.cloudfront.net"

async def request(client, url: str):
    """
    Asynchronously sends a GET request to the specified URL using the provided HTTP client.

    Args:
        client (httpx.AsyncClient): The HTTP client to use for sending the request.
        url (str): The URL to send the GET request to.

    Returns:
        dict: The JSON response from the server.
    """
    headers = {"Content-Type": "application/json"}
    response = await client.get(url, headers=headers)
    return response.json()

async def get_config_layers():
    """
    Asynchronously retrieves the air quality configuration layers from a specified URL.

    Returns:
        dict: The GeoJSON data containing the air quality layers.
    """
    async with httpx.AsyncClient() as client:
        layers = await request(client, AWS_CF_URL + "/air_quality/layers.json")
        return layers

async def get_map_layers():
    """
    Asynchronously retrieves the air quality configuration layers from a specified URL.

    Returns:
        dict: The GeoJSON data containing the air quality layers.
    """
    async with httpx.AsyncClient() as client:
        data = await request(client, AWS_CF_URL + "/air_quality/map.json")
        return data


def filter_layers_by_city(layers: dict, city_name):
    """
    Filters the given layers to include only those that match the specified city name and have a typeMonitoringData of 0.

    Args:
        layers (list): A list of layer dictionaries to filter.
        city_name (str): The name of the city to filter the layers by.

    Returns:
        list: A list of filtered layers that match the city name and typeMonitoringData criteria.
    """
    return [layer for layer in layers if layer.get('cityName') == city_name and layer.get('typeMonitoringData') == 0]

def filter_map_by_key(map_data: dict, entity_key: str):
    """
    Filters the given layers to include only those that match the specified entityKey.

    Args:
        map_data (list): A list of layer dictionaries to filter.
        entity_key (str): The entityKey to filter the layers by.

    Returns:
        list: A list of filtered layers that match the entityKey criteria.
    """
    return [m for m in map_data if m.get('entityKey') == entity_key]

async def get_layers(lat: float, lng: float):
    """
    Asynchronously retrieves the air quality layers for a given latitude and longitude.

    Args:
        lat (float): The latitude of the location.
        lng (float): The longitude of the location.

    Returns:
        dict: The filtered layer data for the specified location, or an error message if no data is available.

    Raises:
        botocore.exceptions.BotoCoreError: If there is an error with the AWS SDK.
        botocore.exceptions.ClientError: If there is an error with the AWS service.
    """
    # get geocoding from open-meteo from coordinates
    location = aws.get_location(lat, lng)
    # get city name from location
    city = location['Municipality']
    # get layers from AWS CloudFront
    layers = await get_config_layers()
    # filter layers by city name
    filtered_layers = filter_layers_by_city(layers, city)
    # return the first filtered layer or an error message if no data is available
    return filtered_layers[0] if filtered_layers else { "error": "No data available for this coordinates [" + str(lat) + ", " + str(lng) + "]" }

async def get_list_geojson(entity_key: str):
    """
    Asynchronously retrieves the list of GeoJSON data containing the air quality layers.

    Returns:
        list: The list of GeoJSON data containing the air quality layers.
    """
    map_data = await get_map_layers()
    filtered_map_data = filter_map_by_key(map_data, entity_key)
    return filtered_map_data