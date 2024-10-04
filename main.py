from fastapi import FastAPI
import ecosensor
app = FastAPI()

@app.get("/air-quality/{lat}/{lng}")
async def root(lat: float, lng: float):
    location, layer = await ecosensor.get_layers(lat, lng)

    if layer.get("error") is not None:
        return layer

    properties = await ecosensor.get_geojson(layer.get('entityKey'), lat, lng)

    return {
        "layer": layer,
        "location": location,
        "data": properties
    }
