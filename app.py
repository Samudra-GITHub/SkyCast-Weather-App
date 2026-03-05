from flask import Flask, render_template, request
import requests
import os # NEW: Needed to talk to Render's environment settings

app = Flask(__name__)

# UPDATED: This tells Python to check Render for "WEATHER_API_KEY" first.
# If it can't find it there, it defaults to your key (backup).
API_KEY = os.environ.get('WEATHER_API_KEY', 'a0e38caf6c6e33fe1904caae30007613')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            url = "https://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric'
            }
            try:
                response = requests.get(url, params=params)
                if response.status_code == 200:
                    weather_data = response.json()
                else:
                    print(f"API Error: {response.status_code}")
            except Exception as e:
                print(f"Connection Error: {e}")

    return render_template('index.html', weather=weather_data)

if __name__ == '__main__':
    # Render will use gunicorn, but this keeps local testing working too
    app.run(debug=True)