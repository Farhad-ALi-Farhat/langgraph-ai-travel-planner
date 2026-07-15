from langchain_core.tools import tool
import requests

from config import OPENWEATHER_API_KEY

@tool
def get_weather(city: str) -> str:
    """Get current weather for a city."""

    api_key = OPENWEATHER_API_KEY

    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units=metric"
    )

    response = requests.get(url).json()

    if "main" in response:
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        return f"{temp}°C, {desc}"

    return "Weather not found"
