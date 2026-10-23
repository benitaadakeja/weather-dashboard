
from flask import Flask, render_template
from datetime import date

app = Flask(__name__)

@app.route("/")
def home():
    temperature = 28
    condition = "Partly cloudy"
    humidity = 72
    city = "Akure"
    today = date.today().strftime("%A, %d %B %Y")
    return render_template("index.html", city=city, today=today, temperature=temperature, condition=condition, humidity=humidity)

if __name__ == "__main__":
    app.run(debug=True)

