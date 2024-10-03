import httpx
import aws

AWS_CF_URL = "https://d17kn6fj50jzfv.cloudfront.net"

async def request(client, url: str):
    headers = {"Content-Type": "application/json"}
    response = await client.get(url, headers=headers)
    return response.json()

async def get_config_layers(city: str):
    async with httpx.AsyncClient() as client:
        geojson_data = await request(client, AWS_CF_URL + "/air_quality/layers.json")

        return geojson_data

async def get_layers(lat: float, lng: float):

    # get geocoding from open-meteo from coordinates
    location = aws.get_location(lat, lng)
    city = location['Municipality']
    layer = await get_config_layers(city)
    return layer