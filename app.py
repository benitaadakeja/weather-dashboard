from datetime import date
import json
import urllib.error
import urllib.request

from flask import Flask, render_template

app = Flask(__name__)

# Stores the last successful weather response while the app is running.
last_weather = None

weather_descriptions = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    80: "Rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    95: "Thunderstorm",
    96: "Thunderstorm with hail",
    99: "Thunderstorm with heavy hail",
}


@app.route("/")
def home():
    global last_weather

    city = "Akure"
    today = date.today().strftime("%A, %d %B %Y")
    weather_notice = None

    try:
        url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=7.25&longitude=5.20"
            "&current=temperature_2m,relative_humidity_2m,weather_code"
            "&timezone=Africa%2FLagos"
        )

        with urllib.request.urlopen(url, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))

        current = data["current"]

        temperature = current["temperature_2m"]
        humidity = current["relative_humidity_2m"]
        weather_code = current["weather_code"]

        condition = weather_descriptions.get(
            weather_code, "Weather condition unknown"
        )

        last_weather = {
            "temperature": temperature,
            "humidity": humidity,
            "condition": condition,
        }

    except (
        urllib.error.URLError,
        TimeoutError,
        ValueError,
        KeyError,
        TypeError,
    ):
        if last_weather is not None:
            temperature = last_weather["temperature"]
            humidity = last_weather["humidity"]
            condition = last_weather["condition"]

            weather_notice = (
                "Unable to refresh weather data. "
                "Showing the last available update."
            )
        else:
            temperature = None
            humidity = None
            condition = None

            weather_notice = (
                "Weather data is temporarily unavailable. "
                "Please try again later."
            )

    return render_template(
        "index.html",
        city=city,
        today=today,
        temperature=temperature,
        humidity=humidity,
        condition=condition,
        weather_notice=weather_notice,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
