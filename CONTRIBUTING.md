# Contributing to SkyCast

Thanks for considering a contribution.

## Getting set up

```bash
git clone https://github.com/Samudra-GITHub/SkyCast-Weather-App.git
cd SkyCast-Weather-App
pip install -r requirements.txt
export OPENWEATHER_API_KEY=your_openweathermap_key
python app.py
```

## Before opening a PR

Manually verify the app runs and a city search returns current weather, forecast, UV, and AQI correctly.

## Scope

- Never commit API keys. `app.py` reads `OPENWEATHER_API_KEY` from the environment and has no fallback; keep it that way.
- Frontend changes belong in `templates/index.html`.

## Reporting issues

Use the issue templates under `.github/ISSUE_TEMPLATE/`.
