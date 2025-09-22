import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry

class WeatherModule:
    def __init__(self, location="Gwalior"):
        self.location = location
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
        retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
        self.openmeteo = openmeteo_requests.Client(session=retry_session)

    def get_real_time_weather(self):
        params = {
            "latitude": 52.52,
            "longitude": 13.41,
            "hourly": ["temperature_2m", "relative_humidity_2m", "weather_code", "dew_point_2m", "precipitation", "uv_index"],
            "models": "best_match",
            "current": ["apparent_temperature", "relative_humidity_2m", "rain", "precipitation"]
        }
        try:
            responses = self.openmeteo.weather_api(self.base_url, params=params)
            response = responses[0]  # Process first location

            current = response.Current()
            weather_info = {
                "temperature": current.Variables(0).Value(),
                "humidity": current.Variables(1).Value(),
                "rainfall": current.Variables(2).Value(),
                "description": "Weather data from Open-Meteo API"
            }
            return weather_info
        except Exception as e:
            return {"error": str(e)}

    def generate_crop_advisory(self, crop):
        weather = self.get_real_time_weather()
        if "error" in weather:
            return f"❌ Error fetching weather data: {weather['error']}"

        advisory = f"📍 Location: {self.location}\\n🌾 Crop: {crop}\\n"
        advisory += f"\\n📊 Weather Data:\\n🌡 Temp: {weather['temperature']}°C\\n💧 Humidity: {weather['humidity']}%\\n🌧 Rainfall (last 1h): {weather['rainfall']}mm\\n🌤️ Condition: {weather['description']}\\n"

        # Advisory logic
        if weather["rainfall"] < 2:
            advisory += "💧 Advice: Consider irrigating the crop.\\n"
        if weather["temperature"] and weather["temperature"] > 35:
            advisory += "🔥 Warning: High temperature! Apply mulch or provide shade.\\n"
        if weather["humidity"] and weather["humidity"] > 80:
            advisory += "⚠️ Caution: High humidity can lead to fungal infections. Monitor crops closely.\\n"

        return advisory
