import requests
import os
from datetime import datetime, timedelta

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
    sunrise_unix_timestamp = data['sys']['sunrise']
    sunset_unix_timestamp = data['sys']['sunset']
    timezone_offset = data['timezone']

    # convert unix timezone neutral timestamp to cooresponding datetime object
    # note datetime.fromtimestamp converts timestamp to computers local timezone. use utcfromtimestamp
    
    sunrise_datetime_object = datetime.utcfromtimestamp(sunrise_unix_timestamp)
    sunset_datetime_object = datetime.utcfromtimestamp(sunset_unix_timestamp)

    # timezone (tz) offset must be done to datetime object before string conversion
    # convert tz to timedelta.

    offset_object = timedelta(seconds=timezone_offset)
    tz_surise = sunrise_datetime_object + offset_object
    tz_surset = sunset_datetime_object + offset_object

    # convert date objects to time string

    sunrise_time = tz_surise.strftime("%H:%M:%S")
    sunset_time = tz_surset.strftime("%H:%M:%S")

    #strptime(sunrise_unix_timestamp, "%H:%M:%S")

    # Display it nicely
    print(f"\n{'='*50}")
    print(f"Weather in {city}, {country}")
    print(f"{'='*50}")
    print(f"Temperature: {temp} C (feels like {feels_like} C)")
    print(f"Conditions: {description.capitalize()}")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} m/s")    
    print(f"Sunrise Time: {sunrise_time}")
    print(f"Sunset Time: {sunset_time}")


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

# Add these features to your weather app:
# - Show sunrise and sunset times (they're in the data as Unix timestamps - look up how to convert them)
# - Add a 5-day forecast feature (use the forecast endpoint: `/data/2.5/forecast`)
# - Let users choose between Celsius and Fahrenheit
# - Save favorite cities and quickly look them up

