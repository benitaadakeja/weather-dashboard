from app import app
def test_homepage_loads():
      with app.test_client() as client:
             response = client.get("/")
             assert response.status_code == 200

def test_homepage_displays_dashboard_title():
      with app.test_client() as client:
          response = client.get("/")
          assert b"Weather Dashboard" in response.data

def test_homepage_displays_weather_data():
      with app.test_client() as client:
           response = client.get("/")
           page = response.get_data(as_text=True)
           assert "Akure" in page 
           assert "28°C" in page
           assert "Partly cloudy"in page
           assert "72%" in page
