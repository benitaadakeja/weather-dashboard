
import urllib.error
import app as weather_app
import json
from unittest.mock import patch
from app import app


def test_homepage_loads():
    with patch("app.urllib.request.urlopen") as mock_urlopen:
        mock_response = mock_urlopen.return_value.__enter__.return_value
        mock_response.read.return_value = json.dumps({
            "current": {
                "temperature_2m": 28,
                "relative_humidity_2m": 72,
                "weather_code": 2
            }
        }).encode("utf-8")

        with app.test_client() as client:
            response = client.get("/")
            assert response.status_code == 200


def test_homepage_displays_dashboard_title():
    with patch("app.urllib.request.urlopen") as mock_urlopen:
        mock_response = mock_urlopen.return_value.__enter__.return_value
        mock_response.read.return_value = json.dumps({
            "current": {
                "temperature_2m": 28,
                "relative_humidity_2m": 72,
                "weather_code": 2
            }
        }).encode("utf-8")

        with app.test_client() as client:
            response = client.get("/")
            assert b"Weather Dashboard" in response.data


def test_homepage_displays_weather_data():
    with patch("app.urllib.request.urlopen") as mock_urlopen:
        mock_response = mock_urlopen.return_value.__enter__.return_value
        mock_response.read.return_value = json.dumps({
            "current": {
                "temperature_2m": 28,
                "relative_humidity_2m": 72,
                "weather_code": 2
            }
        }).encode("utf-8")

        with app.test_client() as client:
            response = client.get("/")
            page = response.get_data(as_text=True)

            assert "Akure" in page
            assert "28°C" in page
            assert "Partly cloudy" in page
            assert "72%" in page

def test_homepage_handles_api_failure_without_cached_weather(monkeypatch):
    monkeypatch.setattr(weather_app, "last_weather", None)

    with patch(
        "app.urllib.request.urlopen",
        side_effect=urllib.error.URLError("Network unavailable"),
    ):
        with app.test_client() as client:
            response = client.get("/")
            page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "Weather data is temporarily unavailable" in page
    assert "Weather details are unavailable right now" in page
def test_homepage_uses_cached_weather_when_api_fails(monkeypatch):
    monkeypatch.setattr(
        weather_app,
        "last_weather",
        {
            "temperature": 29,
            "humidity": 65,
            "condition": "Partly cloudy",
        },
    )

    with patch(
        "app.urllib.request.urlopen",
        side_effect=urllib.error.URLError("Network unavailable"),
    ):
        with app.test_client() as client:
            response = client.get("/")
            page = response.get_data(as_text=True)

    assert response.status_code == 200
    assert "29°C" in page
    assert "65%" in page
    assert "Partly cloudy" in page
    assert "Showing the last available update" in page
