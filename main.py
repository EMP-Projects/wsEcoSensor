from fastapi import FastAPI
import ecosensor
app = FastAPI()

@app.get("/air-quality/{lat}/{lng}")
async def root(lat: float, lng: float):
    layer = await ecosensor.get_layers(lat, lng)
    map_data = await ecosensor.get_list_geojson(layer.get('entityKey'))
    return map_data

