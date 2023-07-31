import requests
from bs4 import BeautifulSoup
import datetime
import re

# surl = "https://www.dvdsreleasedates.com/digital-releases/" # base url

now = datetime.datetime.now()
month_number = now.month
month_name = now.strftime("%B").lower()
year = now.year

url = f"https://www.dvdsreleasedates.com/digital-releases/{year}/{month_number}/digital-hd-releases-{month_name}-{year}"

print(f"url: {url}")

response = requests.get(url)

soup = BeautifulSoup(response.content, "html.parser")
dates = []

for td in soup.find_all("td", class_="reldate"):
    date = td.text.strip().split("\n")[0]
    dates.append(date)

print(f"Dates: {dates}")

today = datetime.date.today().strftime("%A %B %d, %Y")
# today = "Friday July 28, 2023"
print(f"Today's date is: {today}")

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

print(f"Titles: {titles}")