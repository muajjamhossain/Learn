import requests
from plyer import notification

# Replace with your own OpenWeatherMap API key
API_KEY = "your-api-key-here"
CITY = "Patna"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

def get_weather():
    r = requests.get(URL)
    return r.json()

weather_data = get_weather()

# Extract the necessary data from the response
temp = weather_data["main"]["temp"]
rain_chance = weather_data["weather"][0]["description"]

# Format the result string
result = f"Current temperature: {temp}°C in {CITY}\nWeather: {rain_chance}"

# Show the toast notification with the weather update
notification.notify(
    title="Live Weather Update",
    message=result,
    timeout=10
)
