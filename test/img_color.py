from colorthief import ColorThief
import requests

image_url = 'https://image.tmdb.org/t/p/w500//lTZ3r9NBdbrR6NA90v3hFYqd6TC.jpg'
response = requests.get(image_url, stream=True)

if response.status_code == 200:
    # Open the response content as a file-like object
    with response.raw as file:
        # Create a ColorThief instance and get the dominant color
        color_thief = ColorThief(file)
        dominant_color = color_thief.get_color(quality=1)
        print(dominant_color)