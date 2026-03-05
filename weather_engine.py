import requests

def get_weather():
    # 1. SETUP: Enter your details here
    api_key = "a0e38caf6c6e33fe1904caae30007613"
    city = input("Enter the name of a city: ")
    
    # 2. THE URL: This is the address we 'call' to get the data
    # We use f-strings to plug in the city name and api key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    # 3. THE REQUEST: Asking the OpenWeather server for data
    response = requests.get(url)

    # 4. THE RESULT: Checking if the request worked
    if response.status_code == 200:
        data = response.json()  # Convert raw data to a Python Dictionary
        
        # Pulling specific info from the dictionary
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        
        print(f"\nSuccess! The weather in {city.capitalize()} is:")
        print(f"Temperature: {temp}°C")
        print(f"Condition: {description.title()}")
    else:
        print("Error! Could not find city or the API key is still activating.")

# Run the function
get_weather()