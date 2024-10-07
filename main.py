from fastapi import FastAPI
import ecosensor
app = FastAPI()

@app.get("/air-quality/")
async def air_quality(lat: float = None, lng: float = None, city: str = None):
    try :
        if lat is not None and lng is not None:
            return await ecosensor.get_data_by_coordinates(lat, lng)
        elif city is not None:
            return await ecosensor.get_data_by_city(city)
        return {
            "error": "Please provide either latitude and longitude or city name"
        }
    except Exception as e:
        return dict(error=str(e))