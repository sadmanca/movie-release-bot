import requests
import os
from dotenv import load_dotenv
load_dotenv()

TMDB_API_KEY = os.environ["TMDB_API_KEY"]

titles = ['Joy Ride', 'Sympathy for the Devil']

for title in titles:
    response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}')
    if response is not None:
        data = response.json()
        if data['total_results'] > 0:
            movie = data['results'][0]
            print(movie)
            poster_path = movie['poster_path']
            poster_url = f'https://image.tmdb.org/t/p/w500/{poster_path}'
            print(movie['title'])
            print(movie['overview'])
            print(movie['release_date'])
            print(movie['vote_average'])
            print(poster_url)
            print()