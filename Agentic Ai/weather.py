
import requests


def get_weather(city):
    # Get the city's location
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_response = requests.get(
        geo_url,
        params={"name": city, "count": 1},
        timeout=10
    )
    geo_response.raise_for_status()

    places = geo_response.json().get("results", [])

    if not places:
        print("City not found. Please try again.")
        return

    place = places[0]
    latitude = place["latitude"]
    longitude = place["longitude"]

    # Get current weather
    weather_url = "https://api.open-meteo.com/v1/forecast"

    response = requests.get(
        weather_url,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": (
                "temperature_2m,relative_humidity_2m,"
                "apparent_temperature,precipitation,"
                "weather_code,wind_speed_10m"
            ),
            "timezone": "auto"
        },
        timeout=10
    )
    response.raise_for_status()

    data = response.json()["current"]

    descriptions = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Foggy",
        51: "Light drizzle",
        53: "Drizzle",
        55: "Heavy drizzle",
        61: "Light rain",
        63: "Rain",
        65: "Heavy rain",
        71: "Light snow",
        73: "Snow",
        75: "Heavy snow",
        80: "Rain showers",
        81: "Rain showers",
        82: "Heavy rain showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with hail"
    }

    print("\n========== WEATHER REPORT ==========")
    print("City:", place["name"])
    print("Country:", place.get("country", ""))
    print("Temperature:", data["temperature_2m"], "°C")
    print("Feels like:", data["apparent_temperature"], "°C")
    print("Humidity:", data["relative_humidity_2m"], "%")
    print("Wind speed:", data["wind_speed_10m"], "km/h")
    print("Precipitation:", data["precipitation"], "mm")
    print("Condition:", descriptions.get(
        data["weather_code"], "Weather information"
    ))
    print("Time:", data["time"])
    print("====================================")


if __name__ == "__main__":
    city = input("Enter city name: ")

    try:
        get_weather(city.strip())
    except requests.RequestException:
        print("Unable to connect. Check your internet connection.")


