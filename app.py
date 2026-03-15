from flask import Flask, render_template, request, jsonify
import requests
import json
from ai_engine import CropAdvisoryEngine

app = Flask(__name__)

# OpenWeatherMap API Key - Replace with your own key
# Get free key at: https://openweathermap.org/api
import os
from dotenv import load_dotenv
load_dotenv()
WEATHER_API_KEY = os.environ.get("WEATHER_API_KEY")
WEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def fetch_weather(city):
    """Fetch real-time weather data from OpenWeatherMap API"""
    try:
        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }
        response = requests.get(WEATHER_BASE_URL, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            weather_info = {
                "city": data["name"],
                "country": data["sys"]["country"],
                "temperature": round(data["main"]["temp"], 1),
                "feels_like": round(data["main"]["feels_like"], 1),
                "humidity": data["main"]["humidity"],
                "description": data["weather"][0]["description"].title(),
                "wind_speed": data["wind"]["speed"],
                "pressure": data["main"]["pressure"],
                "visibility": data.get("visibility", 0) // 1000,
                "weather_main": data["weather"][0]["main"],
                "icon": data["weather"][0]["icon"]
            }
            return weather_info, None
        elif response.status_code == 404:
            return None, "City not found. Please check the city name and try again."
        elif response.status_code == 401:
            return None, "Invalid API key. Please configure a valid OpenWeatherMap API key."
        else:
            return None, f"Weather service error (Code: {response.status_code}). Please try again."
    
    except requests.exceptions.ConnectionError:
        return None, "Network error. Please check your internet connection."
    except requests.exceptions.Timeout:
        return None, "Request timed out. Please try again."
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    """Main analysis endpoint - IR system query processing"""
    try:
        data = request.get_json()
        city = data.get("city", "").strip()
        soil_moisture = float(data.get("soil_moisture", 50))
        soil_type = data.get("soil_type", "loamy")
        farm_size = data.get("farm_size", "medium")

        if not city:
            return jsonify({"success": False, "error": "Please enter a city name."}), 400

        if not (0 <= soil_moisture <= 100):
            return jsonify({"success": False, "error": "Soil moisture must be between 0 and 100."}), 400

        # Fetch weather (Information Retrieval step)
        weather_data, error = fetch_weather(city)
        if error:
            return jsonify({"success": False, "error": error}), 400

        # Run AI advisory engine
        engine = CropAdvisoryEngine(weather_data, soil_moisture, soil_type, farm_size)
        advice = engine.generate_full_advisory()

        return jsonify({
            "success": True,
            "weather": weather_data,
            "advice": advice
        })

    except ValueError:
        return jsonify({"success": False, "error": "Invalid soil moisture value. Enter a number between 0 and 100."}), 400
    except Exception as e:
        return jsonify({"success": False, "error": f"Analysis failed: {str(e)}"}), 500


@app.route("/health")
def health():
    return jsonify({"status": "running", "system": "Smart Crop Advisory System"})


if __name__ == "__main__":
    print("=" * 60)
    print("  Smart Crop Advisory System")
    print("  IR (Information Retrieval) Project")
    print("=" * 60)
    print("  Server: http://127.0.0.1:5000")
    print("  NOTE: Replace WEATHER_API_KEY in app.py with your key")
    print("        Get free key at: https://openweathermap.org/api")
    print("=" * 60)
    app.run(debug=True, host="0.0.0.0", port=5000)
