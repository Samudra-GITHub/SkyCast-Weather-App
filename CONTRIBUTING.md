# Contributing to SkyCast

Thanks for considering a contribution.

## Getting set up

```bash
git clone https://github.com/Samudra-GITHub/SkyCast-Weather-App.git
cd SkyCast-Weather-App
pip install -r requirements.txt
export WEATHER_API_KEY=your_openweathermap_key
python app.py
```

## Before opening a PR

Manually verify the app runs and a city search returns current weather, forecast, UV, and AQI correctly.

## Scope

- If your change touches `app.py`'s API key handling, remove the hardcoded fallback rather than adding to it.
- Frontend changes belong in `templates/index.html`.

## Reporting issues

Use the issue templates under `.github/ISSUE_TEMPLATE/`.
