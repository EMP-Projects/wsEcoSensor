from datetime import datetime, timedelta
from typing import List, Any

import pyproj
from shapely.geometry import shape
from shapely.ops import nearest_points

import httpx
import pytz
from shapely.geometry.point import Point

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

async def get_data(data: str):
    """
    Asynchronously retrieves the air quality data from a specified URL.

    Returns:
        dict: The GeoJSON data containing the air quality data.
    """
    async with httpx.AsyncClient() as client:
        data = await request(client, AWS_CF_URL + "/air_quality/" + data)
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
    return [layer for layer in layers if layer.get('cityName') == city_name and layer.get('typeMonitoringData') == 'AirQuality']

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
    layers = await get_data("layers.json")
    # filter layers by city name
    filtered_layers = filter_layers_by_city(layers, city)
    # return the first filtered layer or an error message if no data is available
    return filtered_layers[0] if filtered_layers else { "error": "No data available for this coordinates [" + str(lat) + ", " + str(lng) + "]" }

async def get_layers_by_city(city: str):
    """
    Asynchronously retrieves the air quality layers for a given city.

    Args:
        city (str): The name of the city to retrieve the layers for.

    Returns:
        dict: The first layer that matches the city name, or None if no layers match.
    """
    layers = await get_data("layers.json")
    layer = [l for l in layers if l.get('cityName') == city]
    if len(layers) > 0:
        return layer[0]

    return {"error": "No data available for this city [" + city + "]"}

async def get_list_geojson(entity_key: str):
    """
    Asynchronously retrieves the list of GeoJSON data containing the air quality layers.

    Returns:
        list: The list of GeoJSON data containing the air quality layers.
    """
    map_data = await get_data("map.json")
    return filter_map_by_key(map_data, entity_key)

def filter_properties_by_date(properties: dict, start_delta: timedelta = timedelta(minutes=0), end_delta: timedelta = timedelta(hours=1), with_location: bool = True):
    """
    Filters the given properties to include only those that have a date
        dict: A dictionary of filtered properties that have a date greater than the current date.
    """
    try:
        utc = pytz.UTC
        start_date = datetime.now() + start_delta
        end_date = start_date + end_delta
        start_date = utc.localize(start_date).replace(tzinfo=utc)
        end_date = utc.localize(end_date).replace(tzinfo=utc)

        properties_filtered = []

        for p in properties:
            p_date = utc.localize(datetime.strptime(p.get('Date'), "%Y-%m-%dT%H:%M:%SZ")).replace(tzinfo=utc)
            if start_date <= p_date <= end_date:
                if with_location:
                    p["location"] = get_location(p.get("Lat"), p.get("Lng"))
                properties_filtered.append(p)

        return properties_filtered

    except ValueError:
        return {
            "error": ValueError
        }


def create_geographic_point(lat, lng, from_crs='EPSG:4326', to_crs='EPSG:3857'):
    """
    Creates a geographic point from the given latitude and longitude and converts it to the Web Mercator projection (EPSG:3857).

    Args:
        lat (float): The latitude of the geographic point.
        lng (float): The longitude of the geographic point.

    Returns:
        shapely.geometry.Point: The geographic point in the Web Mercator projection.
        :param lng:
        :param lat:
        :param to_crs:
        :param from_crs:
    """
    # Create a geographic point from the given latitude and longitude
    point = Point(lng, lat)

    # Define the WGS 84 coordinate reference system (CRS)
    from_crs_proj = pyproj.CRS(from_crs)

    # Define the Web Mercator projection (CRS)
    to_crs_proj = pyproj.CRS(to_crs)

    # Create a transformer to convert the point from WGS 84 to Web Mercator
    transformer = pyproj.Transformer.from_crs(from_crs_proj, to_crs_proj, always_xy=True)

    # Transform the point to the Web Mercator projection
    point_result = transformer.transform(point.x, point.y)

    # Return the transformed point
    return Point(point_result)

def get_nearest_feature(lat: float, lng: float, features: dict, convert_crs: bool = True):
    """
    Orders the given features by the distance from the specified latitude and longitude.

    Args:
        lat (float): The latitude of the location.
        lng (float): The longitude of the location.
        features (dict): A dictionary of features to order.

    Returns:
        dict: A dictionary of ordered features by the distance from the specified latitude and longitude.
        :param features:
        :param lng:
        :param lat:
        :param convert_crs:
    """
    feature_nearest = None
    min_distance = None
    # create a reference point from the given latitude and longitude
    if convert_crs is True:
        ref_point = create_geographic_point(lng, lat)
    else:
        ref_point = Point(lng, lat)

    # iterate over the features and calculate the distance from the reference point
    for feature in features:
        # get the nearest points on the feature geometry
        p1, p2 = nearest_points(shape(feature["geometry"]), ref_point)
        # calculate the distance between the reference point and the nearest point
        distance = p1.distance(p2)
        # update the minimum distance and nearest feature if necessary
        if (min_distance is None) or (distance < min_distance):
            min_distance = distance
            feature_nearest = feature

    return feature_nearest

def get_location(lat: float, lng: float):
    """
    Retrieves the location from AWS Location Service based on the given latitude and longitude.

    Args:
        lat (float): The latitude of the location.
        lng (float): The longitude of the location.

    Returns:
        dict: The location data from AWS Location Service, or None if the latitude and longitude are invalid.
    """
    # get location from AWS Location Service
    if lat is not None and lng is not None and lat > 0 and lng > 0:
        # create new point from latitude and longitude
        new_point = create_geographic_point(lat, lng, 'EPSG:3857', 'EPSG:4326')
        location = aws.get_location(new_point.y, new_point.x)
        return location
    return None

def get_prediction_values(features: dict, start_delta: timedelta = timedelta(hours=1), end_delta: timedelta = timedelta(days=1), with_location: bool = True):
    properties_max_value = None

    for feature in features:
        properties = feature.get('properties').get('Data')
        if properties is not None:
            # filter properties by field Data with date time greater now plus 1 hour until now plus 1 day
            properties_data_filtered = filter_properties_by_date(properties, start_delta, end_delta)
            # filter properties by field Data with date time greater now
            for p_item in properties_data_filtered:
                # filter properties by field Pollution
                if properties_max_value is None:
                    properties_max_value = p_item
                else:
                    # filter properties by field Pollution
                    if (p_item.get('Pollution') == properties_max_value.get('Pollution') and
                            p_item.get('Value') > properties_max_value.get('Value')):
                        properties_max_value = p_item

    # get location from AWS Location Service
    if with_location:
        properties_max_value["location"] = get_location(properties_max_value.get("Lat"), properties_max_value.get("Lng"))

    return properties_max_value

async def get_data_by(entity_key: str, lat: float = None, lng: float = None):

    map_data = await get_list_geojson(entity_key)

    # create new list to store the filtered data
    now = []

    # create new variable to store the prediction values
    prediction = []

    for data in map_data:
        # get GeoJSON data from the URL
        geojson: Any = await get_data(data.get('data'))
        features: dict | None = geojson.get('features')
        # get prediction values from the GeoJSON data
        prediction.append(get_prediction_values(features))
        if lat is not None and lng is not None:
            # order features by distance from the given latitude and longitude
            feature_nearest = get_nearest_feature(lat, lng, features)
        else:
            # get center from the GeoJSON data
            center = data.get('center')
            feature_nearest = get_nearest_feature(float(center[0]), float(center[1]), features, False)
        # get properties from the nearest feature
        properties = feature_nearest.get('properties').get('Data')
        # filter properties by field Data with date time greater now
        properties_filtered_by_date = filter_properties_by_date(properties)
        for p_date in properties_filtered_by_date:
            now.append(p_date)

    return {
        "now": now,
        "prediction": prediction
    }

async def get_data_by_city(city_name: str):
    """
    Asynchronously retrieves the GeoJSON data containing the air quality layers for a given city.

    Args:
        city_name (str): The name of the city to retrieve the data for.

    Returns:
        dict: The GeoJSON data containing the air quality layers, or an error message if no data is available for the specified city.
    """
    # get layers from AWS CloudFront
    layer = await get_layers_by_city(city_name)
    if layer.get("error") is not None:
        return layer

    return await get_data_by(layer.get('entityKey'))

async def get_data_by_coordinates(lat: float, lng: float):
    """
    Asynchronously retrieves the GeoJSON data containing the air quality layers.

    Returns:
        dict: The GeoJSON data containing the air quality layers.
    """
    layer = await get_layers(lat, lng)

    if layer.get("error") is not None:
        return layer

    return await get_data_by(layer.get('entityKey'), lat, lng)