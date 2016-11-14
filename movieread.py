# movieread.py
# Matthew Cucuzza Troy Ingel
# retrieve the movies from the API

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

    #print js.keys() # retrieves Plot, Rated, Title etc
    #print js.values()

    for x in range(0, len(js['Plot'])):
        plot = js['Plot'].split()

    print plot


    # rated = js["Rated"][0]
    # #response = js["Response"[0]
    # language = js["Language"][0]
    # title = js["Title"][0]
    # country = js["Country"][0]
    # writer = js["Writer"][0]
    # metascore = js["Metascore"][0]
    # imdbRating = js["imdbRating"][0]
    # director = js["Director"][0]
    # released = js["Released"][0]
    # actors = js["Actors"][0]
    # year = js["Year"].split()
    # genre = js["Genre"][0]
    # awards = js["Awards"][0]
    # runtime = js["Runtime"][0]
    # movie_type = js["Type"][0]
    # poster = js["Poster"][0]
    # imdbVotes = js["imdbVotes"][0]
    # imdbID = js["imdbID"][0]

    print('')
    print'url: ',url
