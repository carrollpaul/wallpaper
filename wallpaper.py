import requests
import json
import os
import ctypes
import random
import config

def getWeather() -> None:
    baseUrl = 'http://api.openweathermap.org/data/2.5/weather'
    
    params = {
        'id' : 5393287, # Santa Rosa, CA city ID
        'appid' : config.weatherKey,
        'units' : 'imperial'
    }
    
    r = requests.get(baseUrl, params=params)

    # Check to see if request is good 
    if not r.status_code == 200:
        print("Error")
        return r.status_code

    # Get the description of the current weather, return it 
    text = r.json()
    return text['weather'][0]['description']

def getImage(weather: str) -> None:
    # Search unspash for image with description of current weather 
    baseUrl = 'https://api.unsplash.com/search/photos'
    headers = {
        'Accept-Version' : 'v1',
        'Authorization': f'Client-ID {config.unsplashKey}'
    }
    params = {
        'query' : weather,
        'orientation' : 'landscape',
        'per_page' : 10
    }
    r = requests.get(baseUrl, headers=headers, params=params)
    text = r.json()
    
    # Pick one of ten images at random
    img = random.randint(0, 9)

    # Download URL is necessary to satisfy API requirements
    # Photo URL is where actual photo comes from
    downloadUrl = text['results'][img]['links']['download']
    photoUrl = text['results'][img]['urls']['full']

    # Get image, download it to images folder
    r = requests.get(photoUrl, stream=True)
    with open(f'C:/SourceCode/python/wallpaper/images/{weather}.jpg', 'wb') as f:
        for chunk in r.iter_content(chunk_size=128):
            f.write(chunk)

    # Trigger download endpoint to satisfy API
    r = requests.get(downloadUrl)

def main() -> None: 
    # Get description of weather
    weather = getWeather()
    # Get image of weather
    getImage(weather)
    # Set background image to photo
    ctypes.windll.user32.SystemParametersInfoW(20, 0, f'C:/SourceCode/python/wallpaper/images/{weather}.jpg', 0)

if __name__ == '__main__':
    main()
