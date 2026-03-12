import requests
import os

def get_weather(city):
    """Fetch weather data for a given city"""
    api_key = os.getenv('OPENWEATHER_API_KEY')

    if not api_key:
        print("Error: OPENWEATHER_API_KEY not set")
        return None

    # Build the URL with query parameters
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'  # Use Celsius
    }

    # Make the request
    response = requests.get(base_url, params=params)

    # Check if successful
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print(f"City '{city}' not found")
        return None
    else:
        print(f"Error: {response.status_code}")
        return None

def display_weather(data):
    """Display weather data in a nice format"""
    if not data:
        return

    # Extract the data we want
    city = data['name']
    country = data['sys']['country']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    description = data['weather'][0]['description']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    # Display it nicely
    print(f"\n{'='*50}")
    print(f"Weather in {city}, {country}")
    print(f"{'='*50}")
    print(f"Temperature: {temp} C (feels like {feels_like} C)")
    print(f"Conditions: {description.capitalize()}")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")
    print(f"{'='*50}\n")

def main():
    """Main program loop"""
    print("Weather Lookup App")

    while True:
        city = input("\nEnter a city name (or 'quit' to exit): ")

        if city.lower() == 'quit':
            print("Thanks for using Weather App!")
            break

        weather_data = get_weather(city)
        display_weather(weather_data)

if __name__ == "__main__":
    main()
