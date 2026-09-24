# SkyCast

**Minimal weather dashboard.**

A Flask weather app built around one idea: current conditions, forecast, UV, and air quality — all on one screen, without noise.

<br/>

<img src="./assets/hero-placeholder.svg" width="100%" alt="SkyCast hero" />

<br/>

## Features

- Current conditions for any city
- 5-day / 3-hour forecast (rendered as an hourly + daily view)
- UV index
- Air quality index (AQI)
- Responsive layout

<br/>

## Preview

<table width="100%">
<tr>
<td width="50%"><img src="./assets/screenshot-placeholder.svg" width="100%" alt="Dashboard" /><br/><sub align="center">Dashboard</sub></td>
<td width="50%"><img src="./assets/screenshot-placeholder.svg" width="100%" alt="Forecast view" /><br/><sub align="center">Forecast view</sub></td>
</tr>
</table>

<br/>

## API Integration

Backed by the [OpenWeatherMap API](https://openweathermap.org/api) — current weather and 5-day/3-hour forecast endpoints, combined server-side into a single response the frontend consumes.

<br/>

## Folder Structure

```
skycast/
├── app.py             # Flask app + OpenWeatherMap integration
├── templates/
│   └── index.html
└── requirements.txt
```

<br/>

## Setup

```bash
git clone https://github.com/Samudra-GITHub/SkyCast-Weather-App.git
cd SkyCast-Weather-App
pip install -r requirements.txt
export WEATHER_API_KEY=your_openweathermap_key
python app.py
```

<br/>

## Environment Variables

```bash
WEATHER_API_KEY=   # your OpenWeatherMap API key
```

> **Note:** the current code has a hardcoded fallback API key in `app.py`. That should be removed and the app should fail loudly if `WEATHER_API_KEY` isn't set — a committed key in a public repo is a real exposure risk regardless of whether it's still active.

<br/>

## Tech Stack

`Flask` · `Python` · `Gunicorn` · `OpenWeatherMap API`

<br/>

## Roadmap

- [x] Current weather, forecast, UV, and AQI in one view
- [ ] Remove hardcoded fallback API key
- [ ] Location autocomplete
- [ ] Saved/favorite cities

<br/>

## License

MIT — see [LICENSE](./LICENSE).

<br/>

<sub>Part of the Sams Studio product ecosystem. See the [profile](https://github.com/Samudra-GITHub) for the full lineup.</sub>
