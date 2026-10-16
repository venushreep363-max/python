
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

page = """
<!DOCTYPE html>
<html>
<head>
    <title>Weather Report</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; }

        body {
            margin: 0;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #60a5fa, #c4b5fd);
        }

        .card {
            background: white;
            padding: 30px;
            width: 100%;
            max-width: 480px;
            text-align: center;
            border-radius: 22px;
            box-shadow: 0 10px 30px #0002;
        }

        h1 { color: #3730a3; }
        .subtitle { color: #64748b; }

        form {
            display: flex;
            gap: 8px;
            margin: 25px 0;
        }

        input {
            flex: 1;
            min-width: 0;
            padding: 13px;
            border: 1px solid #cbd5e1;
            border-radius: 9px;
            font-size: 15px;
        }

        button {
            padding: 13px 17px;
            border: none;
            border-radius: 9px;
            background: #4f46e5;
            color: white;
            cursor: pointer;
        }

        button:hover { background: #3730a3; }

        .temperature {
            font-size: 55px;
            font-weight: bold;
            color: #4f46e5;
            margin: 15px;
        }

        .details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-top: 22px;
        }

        .item {
            padding: 12px 8px;
            background: #eef2ff;
            border-radius: 12px;
        }

        .item p { color: #64748b; }
        .error { color: #dc2626; }
        .icon { font-size: 45px; }
        .time { font-size: 12px; color: #64748b; }
    </style>
</head>

<body>
    <div class="card">
        <div class="icon">🌤️</div>
        <h1>Weather Report</h1>
        <p class="subtitle">Check the weather of any city</p>

        <form method="POST">
            <input type="text" name="city"
                   placeholder="Enter city name"
                   value="{{ city }}" required>
            <button type="submit">Search</button>
        </form>

        {% if error %}
            <p class="error">{{ error }}</p>
        {% endif %}

        {% if weather %}
            <h2>{{ weather.city }}, {{ weather.country }}</h2>
            <p>{{ weather.description }}</p>

            <div class="temperature">
                {{ weather.temperature }}°C
            </div>

            <p class="time">Updated: {{ weather.time }}</p>

            <div class="details">
                <div class="item">
                    <h3>🌡️</h3>
                    <p>Feels like</p>
                    <strong>{{ weather.feels }}°C</strong>
                </div>

                <div class="item">
                    <h3>💧</h3>
                    <p>Humidity</p>
                    <strong>{{ weather.humidity }}%</strong>
                </div>

                <div class="item">
                    <h3>💨</h3>
                    <p>Wind speed</p>
                    <strong>{{ weather.wind }} km/h</strong>
                </div>

                <div class="item">
                    <h3>🌧️</h3>
                    <p>Precipitation</p>
                    <strong>{{ weather.rain }} mm</strong>
                </div>
            </div>
        {% else %}
            {% if not error %}
                <p class="subtitle">
                    Enter a city to see its current weather.
                </p>
            {% endif %}
        {% endif %}
    </div>
</body>
</html>
"""


@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    error = None
    city = ""

    if request.method == "POST":
        city = request.form.get("city", "").strip()

        try:
            geo_response = requests.get(
                "https://geocoding-api.open-meteo.com/v1/search",
                params={"name": city, "count": 1},
                timeout=10
            )
            geo_response.raise_for_status()
            places = geo_response.json().get("results", [])

            if not places:
                error = "City not found. Try another city."
            else:
                place = places[0]

                response = requests.get(
                    "https://api.open-meteo.com/v1/forecast",
                    params={
                        "latitude": place["latitude"],
                        "longitude": place["longitude"],
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
                    82: "Heavy showers",
                    95: "Thunderstorm",
                    96: "Thunderstorm with hail",
                    99: "Thunderstorm with hail"
                }

                weather = {
                    "city": place["name"],
                    "country": place.get("country", ""),
                    "temperature": data["temperature_2m"],
                    "feels": data["apparent_temperature"],
                    "humidity": data["relative_humidity_2m"],
                    "wind": data["wind_speed_10m"],
                    "rain": data["precipitation"],
                    "description": descriptions.get(
                        data["weather_code"], "Weather information"
                    ),
                    "time": data["time"].replace("T", " ")
                }

        except requests.RequestException:
            error = "Connection error. Check your internet."

    return render_template_string(
        page, weather=weather, error=error, city=city
    )


if __name__ == "__main__":
    app.run(debug=True)
