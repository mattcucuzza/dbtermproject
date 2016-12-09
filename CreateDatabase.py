# Matt Cucuzza & Troy Ingel
# CSC 325
#
# File executes SQL commands to create the Movie Database in SQLite 

import urllib
import sqlite3

# SQL statements to create tables in the database
# Drops all of the tables first if they exist
# Recreates all of the tables used in the database with their primary keys and references to foreign keys
def createDatabase(cur):
    cur.executescript('''
    DROP TABLE IF EXISTS Acts;
    DROP TABLE IF EXISTS Directs;
    DROP TABLE IF EXISTS Writes;
    DROP TABLE IF EXISTS MovieLanguage;
    DROP TABLE IF EXISTS MovieGenre;
    DROP TABLE IF EXISTS MovieCountry;
    DROP TABLE IF EXISTS Award;
    DROP TABLE IF EXISTS Actor;
    DROP TABLE IF EXISTS Director;
    DROP TABLE IF EXISTS Writer;
    DROP TABLE IF EXISTS Country;
    DROP TABLE IF EXISTS Language;
    DROP TABLE IF EXISTS Genre;
    DROP TABLE IF EXISTS Movie;

    CREATE TABLE Award (
    movie_id INTEGER PRIMARY KEY,
    oscar INTEGER,
    win INTEGER,
    nomination INTEGER,
    FOREIGN KEY(movie_id) REFERENCES Movie(movie_id)
    );

    CREATE TABLE Actor (
    actor_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    actor_first_name TEXT,
    actor_last_name TEXT,
    UNIQUE(actor_first_name,actor_last_name)
    );

    CREATE TABLE Director (
    director_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    director_first_name TEXT,
    director_last_name TEXT
    );

    CREATE TABLE Writer (
    writer_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    first_name TEXT,
    last_name TEXT,
    role TEXT
    );

    CREATE TABLE Country (
    country_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE
    );

    CREATE TABLE Language (
    language_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    language TEXT UNIQUE
    );

    CREATE TABLE Genre (
    genre_id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
    genre_type TEXT UNIQUE
    );

    CREATE TABLE Movie (
    movie_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
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
    FOREIGN KEY(movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY(actor_id) REFERENCES Actor(actor_id)
    );

    CREATE TABLE Directs (
    movie_id INTEGER NOT NULL,
    director_id INTEGER NOT NULL,
    PRIMARY KEY (movie_id, director_id),
    FOREIGN KEY(movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY(director_id) REFERENCES Director(director_id)
    );

    CREATE TABLE Writes (
    movie_id INTEGER NOT NULL,
    writer_id INTEGER NOT NULL,
    PRIMARY KEY (movie_id, writer_id),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (writer_id) REFERENCES Writer(writer_id)
    );

    CREATE TABLE MovieLanguage (
    movie_id INTEGER NOT NULL,
    language_id INTEGER NOT NULL,
    PRIMARY KEY (movie_id, language_id),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (language_id) REFERENCES Language(language_id)
    );

    CREATE TABLE MovieGenre (
    movie_id INTEGER NOT NULL,
    genre_id INTEGER NOT NULL,
    PRIMARY KEY (movie_id, genre_id),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (genre_id) REFERENCES Genre(genre_id)
    );

    CREATE TABLE MovieCountry (
    movie_id INTEGER NOT NULL,
    country_id INTEGER NOT NULL,
    PRIMARY KEY (movie_id, country_id),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id),
    FOREIGN KEY (country_id) REFERENCES Country(country_id)
    );

    ''')
