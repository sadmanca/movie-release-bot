from urllib.request import Request, urlopen
import time
import json
import os

from dotenv import load_dotenv
load_dotenv()

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
    
    titles = ['Joy Ride', 'Sympathy for the Devil']

    movies = json.loads(response_body)
    for movie in movies:
        if movie['movie']['title'] in titles:
            print(movie['movie']['title'])