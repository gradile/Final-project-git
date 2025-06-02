from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = 'b842877a99171f6d11bfc64a15bf0c1b'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    error = None

    if request.method == 'POST':
        city = request.form['city']
        unit = request.form['unit']
        units = 'metric' if unit == 'Celsius' else 'imperial'
        unit_symbol = "°C" if units == "metric" else "°F"

        params = {
            'q': city,
            'appid': API_KEY,
            'units': units
        }

        try:
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            data = response.json()

            weather = {
                'city': data['name'],
                'temperature': f"{data['main']['temp']}{unit_symbol}",
                'feels_like': f"{data['main']['feels_like']}{unit_symbol}",
                'description': data['weather'][0]['description'],
                'humidity': f"{data['main']['humidity']}%",
                'wind_speed': f"{data['wind']['speed']} m/s",
                'icon': f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
            }

        except requests.exceptions.HTTPError:
            error = "City not found or API error."
        except requests.exceptions.RequestException as e:
            error = f"Network error: {e}"

    return render_template('index.html', weather=weather, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

