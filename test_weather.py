import requests
import os

# Get API key from environment
api_key = os.getenv('OPENWEATHER_API_KEY')

if not api_key:
    print("Error: Please set OPENWEATHER_API_KEY environment variable")
    print("  Windows CMD:    set OPENWEATHER_API_KEY=your_key_here")
    print("  Windows PS:     $env:OPENWEATHER_API_KEY = 'your_key_here'")
    print("  Mac/Linux:      export OPENWEATHER_API_KEY=your_key_here")
    exit()

# Make the request
city = "Chicago"
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

response = requests.get(url)

print("Status Code:", response.status_code)
print("\nResponse Data:")
print(response.json())