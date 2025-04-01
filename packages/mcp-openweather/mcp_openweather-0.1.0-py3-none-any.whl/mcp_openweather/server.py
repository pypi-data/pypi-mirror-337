import os
import requests
from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
def current_weather(city: str) -> dict:
    """Query the current weather by city name"""
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("OPENWEATHER_API_KEY environment variable is required")

    base_url = "https://api.openweathermap.org/data/2.5"
    units = "metric"

    try:
        response = requests.get(
            f"{base_url}/weather",
            params={
                "q": city,
                "units": units,
                "appid": api_key
            }
        )
        response.raise_for_status()
        data = response.json()

        formatted_response = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": {
                "current": f"{data['main']['temp']}°C",
                "feels_like": f"{data['main']['feels_like']}°C",
                "min": f"{data['main']['temp_min']}°C",
                "max": f"{data['main']['temp_max']}°C",
            },
            "weather": {
                "main": data["weather"][0]["main"],
                "description": data["weather"][0]["description"],
                "icon": f"https://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
            },
            "details": {
                "humidity": f"{data['main']['humidity']}%",
                "pressure": f"{data['main']['pressure']} hPa",
                "wind_speed": f"{data['wind']['speed']} m/s",
                "wind_direction": f"{data['wind']['deg']}°",
                "cloudiness": f"{data['clouds']['all']}%",
            },
            "sun": {
                "sunrise": datetime.fromtimestamp(data["sys"]["sunrise"]).strftime("%H:%M:%S"),
                "sunset": datetime.fromtimestamp(data["sys"]["sunset"]).strftime("%H:%M:%S"),
            },
            "timestamp": datetime.now().isoformat()
        }

        return formatted_response
    except requests.exceptions.RequestException as e:
        error_message = f"Weather API error: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            error_data = e.response.json()
            if 'message' in error_data:
                error_message = f"Weather API error: {error_data['message']}"
        return {"error": error_message}