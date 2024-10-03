from fastapi import FastAPI
import ecosensor
app = FastAPI()

@app.get("/air-quality/{lat}/{lng}")
async def root(lat: float, lng: float):
    return await ecosensor.get_layers(lat, lng)

