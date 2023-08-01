from urllib.request import Request, urlopen
import json
import requests
from bs4 import BeautifulSoup
import datetime
import re
import time
import os
import platform

from dotenv import load_dotenv
load_dotenv()

WEBHOOK_URL = os.environ["WEBHOOK_URL"]
TMDB_API_KEY = os.environ["TMDB_API_KEY"]
TRAKT_API_KEY = os.environ["TRAKT_API_KEY"]

def get_trakt_watchlist():
    headers = {
        'Content-Type': 'application/json',
        'trakt-api-version': '2',
        'trakt-api-key': os.environ["TRAKT_API_KEY"]
    }
    
    url = os.environ["WATCHLIST_URL"]
    request = Request(url, headers=headers)

    response = None
    start_time = time.time()
    while response is None or response.getcode() != 200:
        try:
            response = urlopen(request)
        except:
            elapsed_time = time.time() - start_time
            if elapsed_time > 900:
                print('Error: Could not connect to server after 15 minutes. Exiting...')
                break
            print(f'Error: Could not connect to server. Retrying in 30 seconds... ({int(elapsed_time)} seconds elapsed)')
            time.sleep(30)
    
    if response is not None:
        response_body = response.read()
        movies = json.loads(response_body)
        return movies

def get_todays_releases():
    now = datetime.datetime.now()
    month_number = now.month
    month_name = now.strftime("%B").lower()
    year = now.year

    url = f"https://www.dvdsreleasedates.com/digital-releases/{year}/{month_number}/digital-hd-releases-{month_name}-{year}"
    print(f"DVD Release Dates URL: {url}\n")
    
    response = requests.get(url)

    soup = BeautifulSoup(response.content, "html.parser")
    dates = []

    for td in soup.find_all("td", class_="reldate"):
        date = td.text.strip().split("\n")[0]
        dates.append(date)
    dates_str = ', '.join(dates)
    print(f"Dates: {dates_str}\n")
        
    if platform.system() == 'Windows':
        today = datetime.date.today().strftime("%A %B %#d, %Y")
    elif platform.system() == 'Linux':
        today = datetime.date.today().strftime("%A %B %-d, %Y")
    print(f"Today's date: {today}\n")
    
    titles = []
    for td in soup.find_all("td", class_="reldate"):
        date = td.text.strip().split("\n")[0]
        if today in date:
            table = td.find_parent("table", class_="fieldtable-inner")
            if table:
                for td in table.find_all("td", class_="dvdcell"):
                    movie_name = td.get_text(strip=True)
                    movie_name = re.sub(r"imdb:.*", "", movie_name)
                    titles.append(movie_name)
            else:
                print("Table not found")
    
    return titles
    
def get_todays_watchlist_releases():
    watchlist = get_trakt_watchlist()
    todays_releases = get_todays_releases()
    
    print(f"watchlist: {watchlist}\n")
    print(f"todays_releases: {todays_releases}\n")
    
    # todays_watchlist_releases = []
    # for movie in watchlist:
    #     if movie['movie']['title'] in todays_releases:
    #         todays_watchlist_releases.append(movie['movie']['title'])
    todays_watchlist_releases = [movie['movie']['title'] for movie in watchlist if movie['movie']['title'] in todays_releases]
    print(f"Today's watchlist releases: {todays_watchlist_releases}\n")
    
    return todays_watchlist_releases

def get_movie_tmdb_metadata(title):
    response = requests.get(f'https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={title}')
    if response is not None:
        data = response.json()
        if data['total_results'] > 0:
            movie = data['results'][0]
            poster_path = movie['poster_path']
            poster_url = f'https://image.tmdb.org/t/p/w500/{poster_path}'
            return movie['title'], movie['overview'], movie['release_date'], movie['vote_average'], poster_url
    return None

def main():
    todays_watchlist_releases = get_todays_watchlist_releases()
    for movie in todays_watchlist_releases:
        title, overview, theatrical_release_date, vote_average, poster_url = get_movie_tmdb_metadata(movie)
        
        body = f"{overview}"
        
        theatrical_release_date = datetime.datetime.strptime(theatrical_release_date, '%Y-%m-%d')
        theatrical_release_date = theatrical_release_date.strftime('%d %B %Y')
        
        digital_release_date = datetime.date.today().strftime('%d %B %Y')
        
        subtitle = f"Rating: {vote_average}/10\nTheatrical Release Date: {theatrical_release_date}\nDigital Release Date: {digital_release_date}"
        
        print(f"Title: {title}")
        print(f"Subtitle: \n{subtitle}")
        print(f"Body: {body}")
        print(f"Poster URL: {poster_url}")
        print()
        
        post_message(title, subtitle, body, image_url=poster_url)

def post_message(title, subtitle, body, image_url):
    """Sends the formatted message to a Discord server.

    Parameters
    ----------
    message : str
        The formatted message to post.

    image_url : str
        The URL used as the thumbnail.

    """

    payload = {
        "username": "movie-release-bot",
        "embeds": [
            {
                "title": title,
                "color": 15548997,
                "description": body,
                "thumbnail": {"url": image_url},
                "footer": {"text": subtitle}
            }
        ]
    }

    with requests.post(WEBHOOK_URL, json=payload) as response:
        print(f"Discord webhook response: {response.status_code}")

if __name__ == "__main__":
    main()