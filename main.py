from fastapi import FastAPI
import ecosensor
app = FastAPI()

@app.get("/air-quality/{lat}/{lng}")
async def air_quality(lat: float, lng: float):
    try :
        location, layer = await ecosensor.get_layers(lat, lng)

        if layer.get("error") is not None:
            return layer

        properties = await ecosensor.get_data_by_coordinates(layer.get('entityKey'), lat, lng)

        return {
            "layer": layer,
            "location": location,
            "data": properties
        }
    except Exception as e:
        return dict(error=str(e))
