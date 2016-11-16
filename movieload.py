import urllib
import sqlite3
import json
import time
import ssl

serviceurl = 'http://www.omdbapi.com/?'
scontext = None

conn = sqlite3.connect('moviedata.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Award;
DROP TABLE IF EXISTS Actor;
DROP TABLE IF EXISTS Director;
DROP TABLE IF EXISTS Writer;
DROP TABLE IF EXISTS Country;
DROP TABLE IF EXISTS Language;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Movie;
DROP TABLE IF EXISTS Acts;
DROP TABLE IF EXISTS Directs;
DROP TABLE IF EXISTS Writes;
DROP TABLE IF EXISTS MovieLanguage;
DROP TABLE IF EXISTS MovieGenre;
DROP TABLE IF EXISTS MovieCountry;
DROP TABLE IF EXISTS MovieAwards;


CREATE TABLE Award (
award_id INTEGER PRIMARY KEY AUTOINCREMENT,
oscar INTEGER,
win INTEGER,
nomination INTEGER
);

CREATE TABLE Actor (
actor_id INTEGER PRIMARY KEY AUTOINCREMENT,
first_name TEXT,
last_name TEXT
);

CREATE TABLE Director (
director_id INTEGER PRIMARY KEY AUTOINCREMENT,
first_name TEXT,
last_name TEXT
);

CREATE TABLE Writer (
writer_id INTEGER PRIMARY KEY AUTOINCREMENT,
first_name TEXT,
last_name TEXT,
role TEXT
);

CREATE TABLE Country (
country_id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT
);

CREATE TABLE Language (
language_id INTEGER PRIMARY KEY AUTOINCREMENT,
type TEXT
);

CREATE TABLE Genre (
genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
type TEXT
);

CREATE TABLE Movie (
id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
title TEXT NOT NULL,
plot TEXT,
runtime INTEGER,
rated TEXT,
release_date DATE,
imdbID INTEGER,
imdbVotes INTEGER,
imdbRating DECIMAL(4,2),
metascore INTEGER
);

CREATE TABLE Acts (
movie_id INTEGER NOT NULL,
actor_id INTEGER NOT NULL,
PRIMARY KEY (movie_id, actor_id),
FOREIGN KEY(movie_id) REFERENCES Movie(id),
FOREIGN KEY(actor_id) REFERENCES Actor(actor_id)
);

CREATE TABLE Directs (
movie_id INTEGER NOT NULL,
director_id INTEGER NOT NULL,
PRIMARY KEY (movie_id, director_id),
FOREIGN KEY(movie_id) REFERENCES Movie(id),
FOREIGN KEY(director_id) REFERENCES Director(director_id)
);

CREATE TABLE Writes (
movie_id INTEGER NOT NULL,
writer_id INTEGER NOT NULL,
PRIMARY KEY (movie_id, writer_id),
FOREIGN KEY (movie_id) REFERENCES Movie(id),
FOREIGN KEY (writer_id) REFERENCES Writer(writer_id)
);

CREATE TABLE MovieLanguage (
movie_id INTEGER NOT NULL,
language_id INTEGER NOT NULL,
PRIMARY KEY (movie_id, language_id),
FOREIGN KEY (movie_id) REFERENCES Movie(id),
FOREIGN KEY (language_id) REFERENCES Language(language_id)
);

CREATE TABLE MovieGenre (
movie_id INTEGER NOT NULL,
genre_id INTEGER NOT NULL,
PRIMARY KEY (movie_id, genre_id),
FOREIGN KEY (movie_id) REFERENCES Movie(id),
FOREIGN KEY (genre_id) REFERENCES Genre(genre_id)
);

CREATE TABLE MovieCountry (
movie_id INTEGER NOT NULL,
country_id INTEGER NOT NULL,
PRIMARY KEY (movie_id, country_id),
FOREIGN KEY (movie_id) REFERENCES Movie(id),
FOREIGN KEY (country_id) REFERENCES Country(country_id)
);

CREATE TABLE MovieAwards (
movie_id INTEGER NOT NULL,
award_id INTEGER NOT NULL,
PRIMARY KEY (movie_id, award_id),
FOREIGN KEY (movie_id) REFERENCES Movie(id),
FOREIGN KEY (award_id) REFERENCES Award(award_id)
)
''')

fh = open("movie_samples.data")
count = 0

for line in fh:
    if count > 200: break
    title = line.strip()
    print ''
    cur.execute("SELECT id FROM Movie WHERE title= ?", (title, ))

    try:
        data = cur.fetchone()[0]
        print "Title Found in DB:", title
        continue
    except:
        pass

    print 'Resolving', title
    url = serviceurl + urllib.urlencode({'t': title,'y':'','plot':'short','r':'json'})
    print 'Retrieving', url
    uh = urllib.urlopen(url, context=scontext)
    data = uh.read()

    print 'Retrieved', len(data), 'characters'
     #data[:20].replace('\n',' ')
    count = count + 1

    try:
        js = json.loads(str(data))
    except:
        continue

    if 'Response' not in js or (js['Response'] != 'True' and js['Response'] != 'ZERO_RESULTS'):
        print '---- FAILURE TO RETRIEVE ----'
        print data
        break

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
    release_date = js["Released"]
    actors = js["Actors"]
    year = js["Year"]
    genre = js["Genre"]
    awards = js["Awards"]
    runtime = js["Runtime"]
    movie_type = js["Type"]
    #poster = js["Poster"]
    imdbVotes = js["imdbVotes"]
    imdbID = js["imdbID"]

    cur.execute('''INSERT OR IGNORE INTO Movie (title, plot, runtime, rated, release_date, imdbID, imdbVotes, imdbRating, metascore)
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? )''', (buffer(title),buffer(plot),buffer(runtime),buffer(rated),buffer(release_date),buffer(imdbID),buffer(imdbVotes),buffer(imdbRating),buffer(metascore) ) )
    #         #data = json file ....

    conn.commit()
    time.sleep(1)

print ""
