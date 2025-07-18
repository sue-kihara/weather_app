from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("OPENWEATHER_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form.get("city")
        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                weather = {
                    "city": data["name"],
                    "country": data["sys"]["country"],
                    "temperature_c": round(data["main"]["temp"], 1),
                    "temperature_f": round((data["main"]["temp"] * 9/5) + 32, 1),
                    "description": data["weather"][0]["description"].title(),
                    "icon": f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
                }
            else:
                error = "City not found. Please try again."
        else:
            error = "Please enter a city name."

    return render_template("index.html", weather=weather, error=error)

if __name__ == "__main__":
    app.run(debug=True)
