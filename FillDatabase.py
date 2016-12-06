# Matt Cucuzza & Troy Ingel
# CSC 325

#import method from another file (make sure they are in same location)
from CreateDatabase import createDatabase
import urllib
import sqlite3
import json
import time
import ssl

#Function that takes a string splits it into firstname + lastname
def splitName(full_name):
    full_name = full_name.strip()
    full_name = full_name.split(" ")
    #if length is 1, only first name
    if len(full_name) == 1:
        firstname = full_name[0]
        lastname = "N/A"
    #if length is 2, middle name not in string
    if len(full_name) == 2:
        firstname = full_name[0]
        lastname = full_name[1]
        #if length is 3, ignore the second item in the list because that is the middle name
    if len(full_name) == 3:
        firstname = full_name[0]
        lastname = full_name[2]
        #if length is longer than 3, firstname is first item, lastname is last item
    if len(full_name) > 3:
        firstname = full_name[0]
        lastname = full_name[-1]
    name_list = [firstname,lastname]
    #Return a list containing firstname + lastname
    return name_list

#Function that takes a string, deletes anything that comes after the name,
#Then performs the same steps as the splitName function above
def handleWriterName(input_str):
    input_str = input_str.split(" (", 1)[0]
    input_str = input_str.split(" ")
    if len(input_str) == 1:
        firstname = input_str[0]
        lastname = "N/A"
    if len(input_str) == 2:
        firstname = input_str[0]
        lastname = input_str[1]
    if len(input_str) == 3:
        firstname = input_str[0]
        lastname = input_str[2]
    if len(input_str) > 3:
        firstname = input_str[0]
        lastname = input_str[-1]
    name_list = [firstname,lastname]
    return name_list

#Function that takes a string, deletes anything that comes before the role,
#If the string contains a "," or "and" or "&" then that means there is more
#than one role listed, and only the first role will be added, else just add
#the whole string because thats the role
def handleWriterRole(input_str):
    #if string has a "(" then the writer has a role listed
    if "(" in input_str:
        #these two split statements remove the "( )" that are around the role
        input_str = input_str.split(" (", 1)[1]
        input_str = input_str.split(")", 1)[0]
        #if "," found, multiple roles are listed, split string and take only first role
        if "," in input_str:
            input_str = input_str.split(",", 1)[0]
        #if "and" found, multiple roles are listed, split string and take only first role
        if "and" in input_str:
            input_str = input_str.split(" and", 1)[0]
        #if "&" found, multiple roles are listed, split string and take only first role
        if "&" in input_str:
            input_str = input_str.split(" &", 1)[0]
        return input_str
    #the string containing the role is returned unless "(" is not found,
    #meaning that the string provided had no role in it, in which case, return "N/A"
    else:
        return "N/A"

#Function to get oscars from a string
def getAwardOscars(input_str):
    #if string contains word "Oscar"
    if "Oscar" in input_str:
        #Split the string on " Oscar", and take the first half of the split (indicated by [0])
        input_str = input_str.split(' Oscar', 1)[0]
        #The string will now have the number at the end of the string, so split the string into a list on each space found
        input_str = input_str.split(" ")
        #return the last item in list because thats where the number will be
        return input_str[-1]
    #if the string does not contain oscar, that means there are 0
    else:
        return "0"

#Function to get wins from a string, (refer to getAwardOscars for step by step explanation)
def getAwardWins(input_str):
    if "win" in input_str:
        input_str = input_str.split(' win', 1)[0]
        input_str = input_str.split(" ")
        return input_str[-1]
    else:
        return "0"

#Function to get nominations from a string, (refer to getAwardOscars for step by step explanation)
def getAwardNominations(input_str):
    if "nomination" in input_str:
        input_str = input_str.split(' nomination', 1)[0]
        input_str = input_str.split(" ")
        return input_str[-1]
    else:
        return "0"

#Print running to the console so you know the program is working
print "----------Running...----------"

#url for retreiving json
serviceurl = 'http://www.omdbapi.com/?'
scontext = None


#connect to the database
conn = sqlite3.connect('moviedata.sqlite')
#define cursor on the database
cur = conn.cursor()
#make sure foreign keys functionality is on
cur.execute('PRAGMA foreign_keys = ON;')

#call method from another file that creates the database and tables (does not populate, just creates)
createDatabase(cur)

#open the file containing the movie names to be imported
movie_file = open("movie_samples.data")


#loop through the file containing movie titles, run a query to see if the title is already in the database,
#if not then make a request to the api to retrive the json information on the movie title
def populateDB():
    line_count = 0
    for line in movie_file:
        if line_count > 200: break
        movie_title = line.strip()
        cur.execute("SELECT movie_id FROM Movie WHERE title= ?", (movie_title, ))

        try:
            data = cur.fetchone()[0]
            print "Movie Already In DB:", movie_title
            continue
        except:
            pass

        #build the url to access the api
        url = serviceurl + urllib.urlencode({'t': movie_title,'y':'','plot':'short','r':'json'})
        uh = urllib.urlopen(url, context=scontext)
        data = uh.read()
        line_count = line_count + 1

        #try to make a request to get json data
        try:
            js_str = json.loads(str(data))
        except:
            continue

        #if statement to handle json failure
        if 'Response' not in js_str or (js_str['Response'] != 'True' and js_str['Response'] != 'ZERO_RESULTS'):
            print '---- FAILURE TO RETRIEVE ----'
            print data
            break

        #setting json response string to corresponding variables
        plot = js_str["Plot"]
        rated = js_str["Rated"]
        language = js_str["Language"]
        title = js_str["Title"]
        country_name = js_str["Country"]
        writer = js_str["Writer"]
        metascore = js_str["Metascore"]
        imdbRating = js_str["imdbRating"]
        director = js_str["Director"]
        release_date = js_str["Released"]
        actors = js_str["Actors"]
        year = js_str["Year"]
        genre = js_str["Genre"]
        awards = js_str["Awards"]
        runtime = js_str["Runtime"]
        movie_type = js_str["Type"]
        imdbVotes = js_str["imdbVotes"]
        imdbID = js_str["imdbID"]


        #Movie - insert all values contained in Movie table
        cur.execute('''INSERT OR IGNORE INTO Movie (title, plot, runtime, rated, release_date, imdbID, imdbVotes, imdbRating, metascore)
                VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? )''', (title,plot,runtime,rated,release_date,imdbID,imdbVotes,imdbRating,metascore) )


        #Actor - insert all values contained in Actor table, then insert movie id and actor id into Acts table (use queries to get foreign key values)
        actors = actors.split(",")
        for a in actors:
            name_list = splitName(a)
            firstname = name_list[0]
            lastname = name_list[1]
            cur.execute('''INSERT OR IGNORE INTO Actor (actor_first_name, actor_last_name)
                    VALUES ( ?, ? )''', (firstname,lastname ) )
            cur.execute('''INSERT OR IGNORE INTO Acts (movie_id,actor_id)
                    VALUES ( (select movie_id from Movie where title = ? and release_date = ?),(select actor_id from Actor where actor_first_name = ? and actor_last_name = ?) )''', (title,release_date, firstname,lastname) )

        #Director - insert all values contained in Director table, then insert movie id and director id into Directs table (use queries to get foreign key values)
        director = director.split(",")
        for d in director:
            name_list = splitName(d)
            firstname = name_list[0]
            lastname = name_list[1]
            cur.execute('''INSERT OR IGNORE INTO Director (director_first_name, director_last_name)
                    VALUES ( ?, ? )''', (firstname,lastname) )
            cur.execute('''INSERT OR IGNORE INTO Directs (movie_id,director_id)
                    VALUES ( (select movie_id from Movie where title = ? and release_date = ?),(select director_id from Director where director_first_name = ? and director_last_name = ?) )''', (title,release_date, firstname,lastname) )

        #Country - insert all values contained in Country table, then insert movie id and country id into MovieCountry table (use queries to get foreign key values)
        country_name = country_name.split(",")
        for c in country_name:
            c = c.strip()
            country = c
            cur.execute('''INSERT OR IGNORE INTO Country (name)
                    VALUES ( ? )''', (country, ) )
            cur.execute('''INSERT OR IGNORE INTO MovieCountry (movie_id,country_id)
                    VALUES ( (select movie_id from Movie where title = ? and release_date = ?),(select country_id from Country where name = ?) )''', (title,release_date,country) )

        #Language - insert all values contained in Language table, then insert movie id and language id into MovieLanguage table (use queries to get foreign key values)
        language = language.split(",")
        for l in language:
            l = l.strip()
            lang = l
            cur.execute('''INSERT OR IGNORE INTO Language (language)
                    VALUES ( ? )''', (lang, ) )
            cur.execute('''INSERT OR IGNORE INTO MovieLanguage (movie_id,language_id)
                    VALUES ( (select movie_id from Movie where title = ? and release_date = ?),(select language_id from Language where language = ?) )''', (title,release_date,lang) )

        #Genre
        genre = genre.split(",")
        for g in genre:
            g = g.strip()
            genre_type = g
            cur.execute('''INSERT OR IGNORE INTO Genre (genre_type)
                    VALUES ( ? )''', (genre_type, ) )
            cur.execute('''INSERT OR IGNORE INTO MovieGenre (movie_id,genre_id)
                    VALUES ( (select movie_id from Movie where title = ? and release_date = ?),(select genre_id from Genre where genre_type = ?) )''', (title,release_date, genre_type) )

        #Writer - insert all values contained in Writer table, then insert movie id and writer id into Writes table (use queries to get foreign key values)
        writer = writer.split(", ")
        for w in writer:
            namelist = handleWriterName(w)
            writerrole = handleWriterRole(w)
            cur.execute('''INSERT OR IGNORE INTO Writer (first_name, last_name,role)
                    VALUES ( ?, ?, ? )''', (namelist[0],namelist[1],writerrole ) )
            cur.execute('''INSERT OR IGNORE INTO Writes (movie_id,writer_id)
                    VALUES ( (select movie_id from Movie where title = ? and release_date = ?),(select writer_id from Writer where first_name = ? and last_name = ? and role = ?) )''', (title,release_date, namelist[0],namelist[1],writerrole) )

        #Awards - insert all values contained in Award table, along with the movie id from Movie table (use queries to get foreign key values)
        cur.execute('''INSERT OR IGNORE INTO Award (movie_id, oscar, win, nomination)
                VALUES ( (select movie_id from Movie where title = ? and release_date = ?),?, ?, ? )''', (title,release_date,int(getAwardOscars(awards)),getAwardWins(awards),getAwardNominations(awards)) )


        #commit the changes to the database
        conn.commit()
        #give user status update
        # print "*** " + title + ": was added !" + " ***"

#Calls method to populate the database
populateDB()

#Housekeeping - close all sources that were opened
movie_file.close()
cur.close()
conn.close()

#print out "Done" to console so user knows when the program has finished
print "-----------Done------------"
