from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = 'b842877a99171f6d11bfc64a15bf0c1b'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

icon_map = {
    '01d': 'wi-day-sunny',
    '01n': 'wi-night-clear',
    '02d': 'wi-day-cloudy',
    '02n': 'wi-night-alt-cloudy',
    '03d': 'wi-cloud',
    '03n': 'wi-cloud',
    '04d': 'wi-cloudy',
    '04n': 'wi-cloudy',
    '09d': 'wi-showers',
    '09n': 'wi-showers',
    '10d': 'wi-day-rain',
    '10n': 'wi-night-rain',
    '11d': 'wi-thunderstorm',
    '11n': 'wi-thunderstorm',
    '13d': 'wi-snow',
    '13n': 'wi-snow',
    '50d': 'wi-fog',
    '50n': 'wi-fog',
}

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
            if 'cod' in data and data['cod'] != 200:
                raise requests.exceptions.HTTPError(data.get('message', 'Error fetching data'))
            
            description = data['weather'][0]['description']
            
            icon_code = data['weather'][0]['icon']
            if data['weather'][0]['icon'] in icon_map:
                icon_class = icon_map[data['weather'][0]['icon']]
            else:
                icon_class = "wi-na"
            weather = {
                'city': data['name'],
                'temperature': f"{data['main']['temp']}{unit_symbol}",
                'feels_like': f"{data['main']['feels_like']}{unit_symbol}",
                'temperature_min': f"{data['main']['temp_min']}{unit_symbol}",
                'temperature_max': f"{data['main']['temp_max']}{unit_symbol}",
                'description': f"{description.capitalize()}",
                'description_icon': data['weather'][0]['icon'],
                'description_class': icon_class,
                'pressure': f"{data['main']['pressure']} hPa",
                'humidity': f"{data['main']['humidity']}%",
                'wind_speed': f"{data['wind']['speed']} m/s",
                'wind_direction': f"{data['wind']['deg']}°",
                'visibility': f"{data['visibility'] / 1000} km",
                'icon_class': icon_map.get(icon_code, 'wi-na')
            }

        except requests.exceptions.HTTPError:
            error = "City not found or API error."
        except requests.exceptions.RequestException as e:
            error = f"Network error: {e}"

    return render_template('index.html', weather=weather, error=error)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)