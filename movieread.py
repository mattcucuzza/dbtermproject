# movieread.py
# Matthew Cucuzza Troy Ingel
# Retrieve Movies and their properies from the OMDB API

import urllib
import json

serviceurl = 'http://www.omdbapi.com/?'

while True:
    movie = raw_input('Enter Movie Title: ')
    if len(movie) < 1: break
    url = serviceurl + urllib.urlencode({'t': movie,'y':'','plot':'short','r':'json'})
    print 'Retrieving', url
    uh = urllib.urlopen(url)

    data = uh.read()
    print 'Retrieved', len(data), 'characters'

    try: js = json.loads(str(data))
    except: js = None

    if 'Response' not in js or js['Response'] != 'True':
        print '---- FAILURE TO RETRIEVE ----'
        print data
        continue

    print json.dumps(js, indent =4)

    plot = js["Plot"]
    rated = js["Rated"]
    # response = js["Response"]
    language = js["Language"]
    title = js["Title"]
    country = js["Country"]
    writer = js["Writer"]
    metascore = js["Metascore"]
    imdbRating = js["imdbRating"]
    director = js["Director"]
    released = js["Released"]
    actors = js["Actors"]
    year = js["Year"]
    genre = js["Genre"]
    awards = js["Awards"]
    runtime = js["Runtime"]
    movie_type = js["Type"]
    poster = js["Poster"]
    imdbVotes = js["imdbVotes"]
    imdbID = js["imdbID"]

    # print plot
    # print rated
    # print language
    # print title
    # print country
    # print writer
    # print metascore
    # print imdbRating
    # print director
    # print released
    # print actors
    # print year
    # print genre
    # print awards
    # print runtime
    # print poster
    # print imdbVotes
    # print imdbID

    print('')
    print'url: ',url
