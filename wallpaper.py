import requests
import json
import os
import ctypes
import time
import glob

def getWeather():
    baseUrl = 'http://api.openweathermap.org/data/2.5/weather?id=5393287&appid=96d97625d6f164e301becd048008122a&units=imperial'
    r = requests.get(baseUrl)

    # Check to see if request is good 
    if not r.status_code == 200:
        print("Error")
        return r.status_code

    # Get the description of the current weather, return it 
    text = r.json()
    return text['weather'][0]['description']

def getImage(weather):
    # Search unspash for image with description of current weather 
    baseUrl = 'https://api.unsplash.com/search/photos'
    headers = {
        'Accept-Version' : 'v1',
        'Authorization': 'Client-ID geRhLJVONz86hhQnvN157X_EnIzovuCqIG9xhilb9rY'
    }
    params = {
        'query' : f'{weather}',
        'orientation' : 'landscape',
        'per_page' : 1
    }
    r = requests.get(baseUrl, headers=headers, params=params)
    text = r.json()
    
    # Download URL is necessary to satisfy API requirements
    # Photo URL is where actual photo comes from
    downloadUrl = text['results'][0]['links']['download']
    photoUrl = text['results'][0]['urls']['full']

    # Get image, download it to images folder
    r = requests.get(photoUrl, stream=True)
    with open(f'C:/SourceCode/python/wallpaper/images/{weather}.jpg', 'wb') as f:
        for chunk in r.iter_content(chunk_size=128):
            f.write(chunk)

    # Trigger download endpoint to satisfy API
    r = requests.get(downloadUrl)

def main():
    while True:
        # Check if image already exists in images folder
        # If image exists, delete it
        dir = glob.glob('C:/SourceCode/python/wallpaper/images')
        if not len(dir) == 0:
            for file in dir:
                os.remove(file)
                
        # Get description of weather
        weather = getWeather()
        # Get image of weather
        getImage(weather)
        # Set background image to photo
        ctypes.windll.user32.SystemParametersInfoW(20, 0, f'C:/SourceCode/python/wallpaper/images/{weather}.jpg', 0)

        time.sleep(24.0 * 60.0 * 60.0)

if __name__ == '__main__':
    main()