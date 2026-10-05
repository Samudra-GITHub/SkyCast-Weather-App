# SkyCast

> A single-screen weather dashboard: current conditions, forecast, UV and air quality for any city, served by a small Flask app.

## Overview

SkyCast takes a city name and shows what matters on one screen without ads or clutter. A Flask backend calls the OpenWeatherMap API, combines several endpoints into one payload, and a single-page front end renders it with an animated sky canvas.

## Features

- Current conditions for any city, with feels-like, min/max, humidity, pressure, visibility, wind and an approximate dew point
- Hourly view (the next 12 three-hour forecast slots, about 36 hours)
- Daily view (up to 7 days, derived from the 5-day / 3-hour forecast)
- UV index and air quality index (AQI, 1 to 5)
- Sunrise, sunset and a day/night flag for the searched location
- Animated sky canvas, with `prefers-reduced-motion` handled in the stylesheet
- A JSON endpoint, `/api/weather?city=...`, which the page uses for searches

## Tech Stack

| Area | Technology |
| --- | --- |
| Backend | Python, Flask, `requests` |
| Frontend | One HTML template with inline CSS and vanilla JavaScript |
| Data | [OpenWeatherMap](https://openweathermap.org/api): current weather, 5-day / 3-hour forecast, air pollution and UV index endpoints |
| Serving | Gunicorn (listed in `requirements.txt`) |

## Project Structure

```
SkyCast-Weather-App/
├── app.py              # Flask app: routes and OpenWeatherMap integration
├── templates/
│   └── index.html      # Entire front end (markup, styles, scripts)
├── assets/             # README placeholder graphics
├── requirements.txt    # Flask, requests, gunicorn
├── .env.example        # Environment variable template
└── README.md
```

## Getting Started

**Prerequisites:** Python 3 and a free [OpenWeatherMap API key](https://openweathermap.org/api).

```bash
git clone https://github.com/Samudra-GITHub/SkyCast-Weather-App.git
cd SkyCast-Weather-App
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Configuration

| Variable | Required | Purpose |
| --- | --- | --- |
| `OPENWEATHER_API_KEY` | Yes | Your OpenWeatherMap API key |

The app has no fallback key and does not load `.env` itself. Export the variable in your shell (`.env.example` is a template, and `.env` is git-ignored):

```bash
export OPENWEATHER_API_KEY=your_key_here      # Windows PowerShell: $env:OPENWEATHER_API_KEY="your_key_here"
```

If it is missing, a search returns a clear "OPENWEATHER_API_KEY is not set" error instead of weather data. Never commit a real key.

## Running Locally

```bash
python app.py        # http://127.0.0.1:5000 (Flask debug mode)
```

Type a city into the search box. The page calls `/api/weather?city=<name>` and renders the result.

## Architecture

`fetch_weather(city)` in `app.py` makes four calls and merges them into one response:

1. Current weather for the city (also yields coordinates and timezone)
2. 5-day / 3-hour forecast, collapsed into an hourly list and per-day min/max buckets
3. Air pollution (AQI)
4. UV index

| Route | Method | Purpose |
| --- | --- | --- |
| `/` | GET, POST | Serves the page; a POSTed `city` is rendered server-side |
| `/api/weather` | GET | JSON weather for `?city=`. Returns 400 if missing, 404 if not found, 503 if the API key is not configured |

## Deployment

No deployment configuration is included. Gunicorn is in `requirements.txt`, so a typical setup is `gunicorn app:app` with `OPENWEATHER_API_KEY` set as an environment variable on the host.

## Screenshots

`assets/` holds placeholder graphics only, so no screenshots are shown.

## Future Improvements

- Location autocomplete
- Saved or favourite cities
- Automated tests

## License

MIT, see [LICENSE](LICENSE).
