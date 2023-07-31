import json

response_body = b'[{"rank":1,"id":864660981,"listed_at":"2023-07-14T02:22:10.000Z","notes":null,"type":"movie","movie":{"title":"Blue Beetle","year":2023,"ids":{"trakt":415437,"slug":"blue-beetle-2023","imdb":"tt9362930","tmdb":565770}}},{"rank":2,"id":875345532,"listed_at":"2023-07-31T15:15:06.000Z","notes":null,"type":"movie","movie":{"title":"Sympathy for the Devil","year":2023,"ids":{"trakt":829228,"slug":"sympathy-for-the-devil-2023","imdb":"tt21991654","tmdb":1030987}}},{"rank":3,"id":853568262,"listed_at":"2023-06-24T04:45:09.000Z","notes":null,"type":"movie","movie":{"title":"Back to the Future","year":1985,"ids":{"trakt":74,"slug":"back-to-the-future-1985","imdb":"tt0088763","tmdb":105}}},{"rank":4,"id":860083524,"listed_at":"2023-07-05T23:10:59.000Z","notes":null,"type":"movie","movie":{"title":"Indiana Jones and the Temple of Doom","year":1984,"ids":{"trakt":56,"slug":"indiana-jones-and-the-temple-of-doom-1984","imdb":"tt0087469","tmdb":87}}}]'

titles = ['Joy Ride', 'Sympathy for the Devil']

movies = json.loads(response_body)
for movie in movies:
    if movie['movie']['title'] in titles:
        print(movie['movie']['title'])