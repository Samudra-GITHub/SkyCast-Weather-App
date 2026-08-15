from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get('WEATHER_API_KEY', 'a0e38caf6c6e33fe1904caae30007613')
BASE = "https://api.openweathermap.org"


def fetch_weather(city):
    """
    Fetches current weather, 5-day/3-hour forecast, UV index, and AQI.
    Returns a single dict with all data needed by the frontend, or None on error.
    """

    # ── 1. Current weather ──────────────────────────────────────────────────
    cur_resp = requests.get(
        f"{BASE}/data/2.5/weather",
        params={"q": city, "appid": API_KEY, "units": "metric"},
        timeout=8,
    )
    if cur_resp.status_code != 200:
        return None

    cur = cur_resp.json()
    lat = cur["coord"]["lat"]
    lon = cur["coord"]["lon"]
    timezone_offset = cur["timezone"]  # seconds offset from UTC

    # ── 2. 5-day / 3-hour forecast (gives hourly-ish + daily) ──────────────
    fc_resp = requests.get(
        f"{BASE}/data/2.5/forecast",
        params={"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"},
        timeout=8,
    )
    forecast_list = fc_resp.json().get("list", []) if fc_resp.status_code == 200 else []

    # Build hourly (next 12 slots = 36 hours)
    hourly = []
    for item in forecast_list[:12]:
        hourly.append({
            "dt": item["dt"],
            "temp": item["main"]["temp"],
            "description": item["weather"][0]["description"],
            "icon": item["weather"][0]["icon"],
            "pop": item.get("pop", 0),          # probability of precipitation 0-1
            "humidity": item["main"]["humidity"],
        })

    # Build daily — collapse 3-hour slots into per-day buckets
    from collections import defaultdict
    from datetime import datetime, timezone, timedelta

    tz = timezone(timedelta(seconds=timezone_offset))
    daily_buckets = defaultdict(list)
    for item in forecast_list:
        dt_local = datetime.fromtimestamp(item["dt"], tz=tz)
        key = dt_local.strftime("%Y-%m-%d")
        daily_buckets[key].append(item)

    daily = []
    for day_key in sorted(daily_buckets.keys())[:7]:
        slots = daily_buckets[day_key]
        temps = [s["main"]["temp"] for s in slots]
        pops  = [s.get("pop", 0) for s in slots]
        # Pick the midday slot description (or first available)
        mid = slots[len(slots) // 2]
        daily.append({
            "dt": slots[0]["dt"],
            "temp_min": min(temps),
            "temp_max": max(temps),
            "description": mid["weather"][0]["description"],
            "icon": mid["weather"][0]["icon"],
            "pop": max(pops),
        })

    # ── 3. Air Quality Index ────────────────────────────────────────────────
    aqi = 1  # default "Good"
    aqi_resp = requests.get(
        f"{BASE}/data/2.5/air_pollution",
        params={"lat": lat, "lon": lon, "appid": API_KEY},
        timeout=6,
    )
    if aqi_resp.status_code == 200:
        aqi_data = aqi_resp.json()
        try:
            aqi = aqi_data["list"][0]["main"]["aqi"]  # 1-5
        except (KeyError, IndexError):
            pass

    # ── 4. One Call API for UV index (free tier) ────────────────────────────
    uvi = 0
    onecall_resp = requests.get(
        f"{BASE}/data/2.5/uvi",
        params={"lat": lat, "lon": lon, "appid": API_KEY},
        timeout=6,
    )
    if onecall_resp.status_code == 200:
        uvi = onecall_resp.json().get("value", 0)

    # ── 5. Assemble final payload ───────────────────────────────────────────
    main = cur["main"]
    wind = cur.get("wind", {})
    sys  = cur.get("sys", {})
    weather_desc = cur["weather"][0]

    # Determine if it's daytime at the location
    now_unix = cur.get("dt", 0)
    is_day = sys.get("sunrise", 0) <= now_unix <= sys.get("sunset", 0)

    return {
        "current": {
            "name":        cur["name"],
            "country":     sys.get("country", ""),
            "lat":         lat,
            "lon":         lon,
            "temp":        main["temp"],
            "feels_like":  main["feels_like"],
            "temp_min":    main["temp_min"],
            "temp_max":    main["temp_max"],
            "humidity":    main["humidity"],
            "pressure":    main["pressure"],
            "visibility":  cur.get("visibility", 10000),
            "wind_speed":  wind.get("speed", 0),
            "wind_deg":    wind.get("deg", 0),
            "description": weather_desc["description"],
            "icon":        weather_desc["icon"],
            "timezone":    timezone_offset,
            "sunrise":     sys.get("sunrise", 0),
            "sunset":      sys.get("sunset", 0),
            "is_day":      is_day,
            "uvi":         round(uvi, 1),
            "dew_point":   round(
                main["temp"] - ((100 - main["humidity"]) / 5), 1
            ),  # Magnus approximation
            "aqi":         aqi,
        },
        "hourly": hourly,
        "daily":  daily,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error   = None
    city    = ""

    if request.method == "POST":
        city = request.form.get("city", "").strip()
        if city:
            weather = fetch_weather(city)
            if weather is None:
                error = f"City \"{city}\" not found. Check the spelling and try again."

    return render_template("index.html", weather=weather, error=error, city=city)


@app.route("/api/weather")
def api_weather():
    """JSON endpoint — used by the JS live-search in the template."""
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"error": "city required"}), 400
    data = fetch_weather(city)
    if data is None:
        return jsonify({"error": "city not found"}), 404
    return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
