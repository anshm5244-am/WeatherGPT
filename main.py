from fastapi import FastAPI, HTTPException, Query  
from fastapi.middleware.cors import CORSMiddleware  
import httpx 

# ============================================================
# OPEN-METEO API URLs
# ============================================================

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"


# ============================================================
# FASTAPI APP
# ============================================================

app = FastAPI(
    title="Weather Backend",
    version="2.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# ROOT / HEALTH CHECK
# ============================================================

@app.get("/")
async def root():
    return {
        "status": "ok",
        "message": "Weather backend is running with Open-Meteo"
    }


# ============================================================
# FIND CITY COORDINATES
# ============================================================

async def get_coordinates(city: str):

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                GEOCODING_URL,
                params=params
            )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Geocoding request timed out."
        )

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Error contacting Open-Meteo: {str(e)}"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail="Unable to find city."
        )

    data = response.json()

    if not data.get("results"):
        raise HTTPException(
            status_code=404,
            detail=f"City '{city}' not found."
        )

    location = data["results"][0]

    return {
        "name": location.get("name", city),
        "country": location.get("country"),
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "timezone": location.get("timezone")
    }


# ============================================================
# CURRENT WEATHER
#
# Example:
# /weather?city=Mumbai
# ============================================================

@app.get("/weather")
async def get_weather(
    city: str = Query(
        ...,
        min_length=1,
        description="City name"
    )
):

    location = await get_coordinates(city)

    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],

        "current": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "weather_code,"
            "wind_speed_10m,"
            "surface_pressure"
        ),

        "timezone": "auto"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                WEATHER_URL,
                params=params
            )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Weather API request timed out."
        )

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Error contacting Open-Meteo: {str(e)}"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Open-Meteo API error: {response.text}"
        )

    data = response.json()

    try:
        current = data["current"]

        return {
            "city": location["name"],
            "country": location["country"],

            "temperature_c": current["temperature_2m"],

            "feels_like_c": current["apparent_temperature"],

            "humidity_percent": current["relative_humidity_2m"],

            "pressure_hpa": current["surface_pressure"],

            "weather_code": current["weather_code"],

            "wind_speed_kmh": current["wind_speed_10m"],

            "timezone": data.get(
                "timezone",
                location["timezone"]
            )
        }

    except KeyError:
        raise HTTPException(
            status_code=502,
            detail="Unexpected response format from Open-Meteo."
        )


# ============================================================
# 5-DAY FORECAST
#
# Example:
# /forecast?city=Mumbai
# ============================================================

@app.get("/forecast")
async def get_forecast(
    city: str = Query(
        ...,
        min_length=1,
        description="City name"
    )
):

    location = await get_coordinates(city)

    params = {
        "latitude": location["latitude"],
        "longitude": location["longitude"],

        "hourly": (
            "temperature_2m,"
            "relative_humidity_2m,"
            "weather_code,"
            "wind_speed_10m"
        ),

        "forecast_days": 5,

        "timezone": "auto"
    }

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                WEATHER_URL,
                params=params
            )

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Forecast request timed out."
        )

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Error contacting Open-Meteo: {str(e)}"
        )

    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"Open-Meteo API error: {response.text}"
        )

    data = response.json()

    try:
        hourly = data["hourly"]

        forecast_list = []

        for i in range(len(hourly["time"])):

            forecast_list.append({
                "datetime": hourly["time"][i],

                "temperature_c":
                    hourly["temperature_2m"][i],

                "humidity_percent":
                    hourly["relative_humidity_2m"][i],

                "weather_code":
                    hourly["weather_code"][i],

                "wind_speed_kmh":
                    hourly["wind_speed_10m"][i]
            })

        return {
            "city": location["name"],
            "country": location["country"],
            "forecast": forecast_list
        }

    except KeyError:
        raise HTTPException(
            status_code=502,
            detail="Unexpected response format from Open-Meteo."
        )


# ============================================================
# RUN SERVER
# ============================================================

if __name__ == "__main__":

    import uvicorn 
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
  )
