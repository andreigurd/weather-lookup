import requests
import os
from datetime import datetime, timedelta, timezone
import json
from tabulate import tabulate

# set global default units
units = 'metric'
temp_units = 'C'
speed_units = 'm/s'

#--------------------------------------------------------------------------------------
#   opening favorites json file
#--------------------------------------------------------------------------------------
try:
    with open('favorites.json', 'r') as file:
        favorites = json.load(file)
except FileNotFoundError:
    print("Favorites file not found. Blank list created.")
    favorites = [] # makes an empty list
except json.JSONDecodeError:
    print("Issue loading favorites file. File empty or invalid JSON file. Blank favorites list created.")
    favorites = []
except ValueError:
    print("Invalid favorites city item. Blank list created.")
    favorites = []
except PermissionError:
    print("Need permission to access favorites file. Blank favorites list created.")
    favorites = []

#--------------------------------------------------------------------------------------
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
        'units': units  
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

#-----------------------------------------------------------------------    
def get_forecast(city):
    """Fetch forecast data for a given city"""
    api_key = os.getenv('OPENWEATHER_API_KEY')
    
    if not api_key:
        print("Error: OPENWEATHER_API_KEY not set")
        return None
    
    # Build the URL with query parameters
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        'q': city,
        'appid': api_key,
        'units': units
    }
    
    # Make the request
    response = requests.get(base_url, params=params)
    
    # print json data keys    
    # data = response.json()
    # print(data.keys())
    # #print(json.dumps(data, indent=2)) # may not be helpfull to print everything

    # # can print limited entries in keys to see data structure
    # #[:xx] limits to number of entries in data list.
    # print(json.dumps(data['city'], indent=2))
    # print(json.dumps(data['cnt'], indent=2))
    # print(json.dumps(data['list'][:0], indent=2))       

    # Check if successful
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 404:
        print(f"City '{city}' not found")
        return None
    else:
        print(f"Error: {response.status_code}")
        return None
    
    
#-----------------------------------------------------------------------
def display_weather(data):
    # weather_data was sent to this function in main with "display_weather(weather_data)" so now weather_data = data
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
    # note utcfromtimestamp (not timezone aware) returns no tz info attached. python prefers datetime.fromtimestamp()
    
    sunrise_datetime_object = datetime.fromtimestamp(sunrise_unix_timestamp, tz=timezone.utc)
    sunset_datetime_object = datetime.fromtimestamp(sunset_unix_timestamp, tz=timezone.utc)

    # timezone (tz) offset must be done to datetime object before string conversion
    # convert tz to timedelta.

    offset_object = timedelta(seconds=timezone_offset)
    tz_sunrise = sunrise_datetime_object + offset_object
    tz_sunset = sunset_datetime_object + offset_object

    # convert date objects to time string

    sunrise_time = tz_sunrise.strftime("%H:%M:%S")
    sunset_time = tz_sunset.strftime("%H:%M:%S")

    #strptime(sunrise_unix_timestamp, "%H:%M:%S")

    # Display it nicely
    print(f"\n{'='*50}")
    print(f"Weather in {city}, {country}")
    print(f"{'='*50}")
    print(f"Temperature: {temp} {temp_units} (feels like {feels_like} {temp_units})")
    print(f"Conditions: {description.capitalize()}")
    print(f"Humidity: {humidity}%")
    print(f"Wind Speed: {wind_speed} {speed_units}")    
    print(f"Sunrise Time: {sunrise_time}")
    print(f"Sunset Time: {sunset_time}")

#-----------------------------------------------------------------------
def display_forecast(data):
    """Display weather data in a nice format"""
    if not data:
        return

    # Extract the data we want
    #city and country listed only once.
    city = data['city']['name']
    country = data['city']['country']

    # loop through each entry
    print(f"\n{'='*50}")
    print(f"Forecast for {city}, {country}")
    print(f"{'='*50}")    

    for entry in data['list']:
        #print(entry.keys())
        date_stmp = entry['dt']        
        datetime_object = datetime.fromtimestamp(date_stmp, tz=timezone.utc)        
        date_string = datetime_object.strftime("%Y-%m-%d %H:%M")      
        temp = entry['main']['temp']        
        humidity = entry['main']['humidity']        
        wind_speed = entry['wind']['speed']

        print(f"\nDate: {date_string}")
        print(f"Temperature: {temp} {temp_units}")
        print(f"Humidity: {humidity}%")
        print(f"Wind Speed: {wind_speed} {speed_units}")      
    
    
def choose_favorite():
    
    numbered_list = []    
    for number, city_item in enumerate(favorites, start=1):
            numbered_favs = {
            "number": number,
            "city" : city_item["favorite city"],            
            }                
            numbered_list.append(numbered_favs)

    print(tabulate(numbered_list, headers="keys", tablefmt="grid"))
    while True:
        try:            
            city_number = int(input("Select City # from Favorites:\n"))
            if 1 <= city_number and city_number <= len(numbered_list):
                        break
            else:
                    print("Number out of range. Please try again.")
        except ValueError:
            print("Invalid entry. Please try again.")

    city = favorites[city_number - 1]["favorite city"]
    return city
#--------------------------------------------------------------------------------------

def create_favorit():
    fav_city = input("Enter City to save as one of favorites:")
    favorites_item = {"favorite city": fav_city}
    if favorites_item not in favorites:
        favorites.append(favorites_item)   

#--------------------------------------------------------------------------------------
#   function to write to favorites json
#--------------------------------------------------------------------------------------
def write_json():
    with open('favorites.json', 'w') as file:
        json.dump(favorites, file, indent=4)

#--------------------------------------------------------------------------------------
def main():
    """Main program loop"""
    print("Weather Lookup App")
    global units, temp_units, speed_units

    while True:
        print("\nOptions:")
        print("[0] Quit")
        print("[1] Enter City")
        print("[2] Select from Favorite Cities")
        print("[3] Save a Favorite City")
        
        menu_option = input("Select option:")

        if menu_option == "0":
            print("Thanks for using Weather App!")
            return
    
        elif menu_option == "1":
            city = input("\nEnter a city name : ") 
            break
        elif menu_option == "2":            
            if len(favorites) == 0:
                print("No favorites exist yet.")
                continue
            city = choose_favorite()
            break
        elif menu_option == "3":
            create_favorit()
            write_json() 
            continue
        else:
            print("Invalid option. Try again.")

    while True: 
        option = input("\nEnter Metric or Imperial units to display: ").lower()
        if option == "metric":
            units = option
            temp_units = 'C'
            speed_units = 'm/s'
            break            
        elif option == "imperial":
            units = option
            temp_units = 'F'
            speed_units = 'mph'
            break            
        else:
            print("Invalid option. Please select from the two options.")
            continue
        
    while True:
        option = input("\nEnter Weather or Forecast lookup: ").lower()
        if option == "weather":
            weather_data = get_weather(city)
            display_weather(weather_data) # this sends weather_data into the function display_weather
            break
        elif option == "forecast":
            forecast_data = get_forecast(city)
            display_forecast(forecast_data)
            break
        else:
            print("Invalid option. Please select from the two options.")
            continue

    return (units, temp_units, speed_units)


if __name__ == "__main__":
    main()

# Add these features to your weather app:
# - Show sunrise and sunset times (they're in the data as Unix timestamps - look up how to convert them)
# - Add a 5-day forecast feature (use the forecast endpoint: `/data/2.5/forecast`)
# - Let users choose between Celsius and Fahrenheit
# - Save favorite cities and quickly look them up

