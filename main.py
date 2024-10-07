from fastapi import FastAPI
import ecosensor
app = FastAPI()

@app.get("/air-quality/")
async def air_quality(lat: float = None, lng: float = None, city: str = None, query: str = None):
    try :
        if lat is not None and lng is not None:
            return await ecosensor.get_data_by_coordinates(lat, lng)
        elif city is not None:
            return await ecosensor.get_data_by_city(city)
        elif query is not None:
            return await ecosensor.get_data_by_query(query)
        return {
            "error": "Please provide either latitude and longitude, city name or query."
        }
    except Exception as e:
        return dict(error=str(e))