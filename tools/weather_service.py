from urllib.parse import quote
from urllib.request import Request, urlopen
import json


class WeatherService:
    """
    Dependency-free Open-Meteo weather service for JARVIS V5.
    """

    FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"

    WEATHER_CODES = {
        0: "clear sky",
        1: "mainly clear",
        2: "partly cloudy",
        3: "overcast",
        45: "fog",
        48: "depositing rime fog",
        51: "light drizzle",
        53: "moderate drizzle",
        55: "dense drizzle",
        56: "light freezing drizzle",
        57: "dense freezing drizzle",
        61: "slight rain",
        63: "moderate rain",
        65: "heavy rain",
        66: "light freezing rain",
        67: "heavy freezing rain",
        71: "slight snow fall",
        73: "moderate snow fall",
        75: "heavy snow fall",
        77: "snow grains",
        80: "slight rain showers",
        81: "moderate rain showers",
        82: "violent rain showers",
        85: "slight snow showers",
        86: "heavy snow showers",
        95: "thunderstorm",
        96: "thunderstorm with slight hail",
        99: "thunderstorm with heavy hail",
    }

    def _get_json(self, url):
        request = Request(
            url,
            headers={
                "User-Agent": "JARVIS-V5/1.0",
                "Accept": "application/json",
            },
        )

        with urlopen(request, timeout=10) as response:
            if response.status != 200:
                raise RuntimeError(
                    f"Weather service returned HTTP {response.status}"
                )

            return json.loads(response.read().decode("utf-8"))

    def geocode(self, city):
        """
        Resolve a city name into latitude/longitude.
        """

        if not city:
            return None

        url = (
            f"{self.GEOCODING_URL}"
            f"?name={quote(city)}"
            f"&count=1"
            f"&language=en"
            f"&format=json"
        )

        data = self._get_json(url)
        results = data.get("results") or []

        if not results:
            return None

        result = results[0]

        return {
            "name": result.get("name", city),
            "country": result.get("country", ""),
            "latitude": result["latitude"],
            "longitude": result["longitude"],
        }

    def get_current_weather(self, city):
        """
        Return current weather for a city.
        """

        location = self.geocode(city)

        if not location:
            return {
                "success": False,
                "message": (
                    f"Sir, I couldn't find a location named {city}."
                ),
            }

        url = (
            f"{self.FORECAST_URL}"
            f"?latitude={location['latitude']}"
            f"&longitude={location['longitude']}"
            "&current=temperature_2m,"
            "relative_humidity_2m,"
            "apparent_temperature,"
            "weather_code,"
            "wind_speed_10m"
            "&timezone=auto"
        )

        data = self._get_json(url)
        current = data.get("current")

        if not current:
            return {
                "success": False,
                "message": (
                    "Sir, the weather service did not return "
                    "current weather data."
                ),
            }

        code = current.get("weather_code")
        description = self.WEATHER_CODES.get(
            code,
            "unknown conditions",
        )

        return {
            "success": True,
            "city": location["name"],
            "country": location["country"],
            "temperature": current.get("temperature_2m"),
            "feels_like": current.get("apparent_temperature"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_speed": current.get("wind_speed_10m"),
            "description": description,
            "time": current.get("time"),
        }

    def answer(self, city):
        """
        Produce a concise voice-friendly weather answer.
        """

        try:
            weather = self.get_current_weather(city)
        except Exception as exc:
            print(f"Weather service error: {exc}")

            return (
                "Sorry, sir. I couldn't access the weather "
                "service right now."
            )

        if not weather["success"]:
            return weather["message"]

        return (
            f"Sir, the current weather in {weather['city']} is "
            f"{weather['temperature']} degrees Celsius, "
            f"feels like {weather['feels_like']} degrees, "
            f"with {weather['description']}. "
            f"Humidity is {weather['humidity']} percent, "
            f"and wind speed is {weather['wind_speed']} "
            f"kilometers per hour."
        )
