# Matthew Cucuzza & Troy Ingel
# CSC325
#
# File creates the GUI for the Movie Database program and allows the user to insert, delete, and query the database

from Tkinter import *
import ttk
from FillDatabase import *
import sqlite3

# Creates the TKinter GUI with the dimensions, and sets the title
root = Tk()
root.geometry("1170x700")
root.title('Movies Database')

# Array of labels to be recursively created
y_labels = ['Movie Title:', 'Actor (Last Name):', 'Genre:', 'Director (Last Name):', 'Plot:', 'Release Date:', 'Rated:', 'IMDb Rating:', 'Writer (Last Name):', 'Oscars:']

title = Label(root, text="Movies Database", font=("Helvetica", 25))
title.grid(row=0, column=1)
tree = NoneType

# Creates the frame for the bottom labels and entry fields
BottomFrame = Frame(root, bg="white", height=500, width=700, padx=20)
BottomFrame.pack(side=LEFT, expand=1)
BottomFrame.grid(row=15, column=1)

#Connects to SQLite, fetches all movies, and fetches all the columns
conn = sqlite3.connect('moviedata.sqlite')
cur = conn.cursor()
fetch = cur.execute("SELECT * FROM Movie").fetchall()
columns = [column[0] for column in cur.description]
results = []

# Method to clear all of the entry fields
def clearFields():
    movie_title_entry.delete(0,END)
    actor_entry.delete(0,END)
    genre_entry.delete(0,END)
    director_entry.delete(0,END)
    plot_entry.delete(0,END)
    release_date_entry.delete(0,END)
    rated_entry.delete(0,END)
    imdb_rating_entry.delete(0,END)
    writer_entry.delete(0,END)
    oscars_entry.delete(0,END)

# Method to create the treeview
def createTree(column, data):
    global tree
    if tree != NoneType:
        tree.destroy()

    # Creates the tree
    tree = ttk.Treeview(columns=column, show='headings')
    tree.pack(expand=YES, fill=BOTH)

    # Loops through the columns and sets them in the headers of the treeview
    for c in column:
        tree.heading(c, text=c.title())
        tree.column(c, width=115, stretch=True)

    # Loops through all of the data and stores it into the treeview
    for d in data:
        tree.insert('', 'end', values=d)

    # Allows scrolling vertically and horizontally
    y_scroll = ttk.Scrollbar(orient=VERTICAL, command=tree.yview)
    x_scroll = ttk.Scrollbar(orient=HORIZONTAL, command=tree.xview)
    tree['yscroll'] = y_scroll.set
    tree['xscroll'] = x_scroll.set

    tree.grid(row=5, column=1, columnspan=100, sticky=W, padx=10)

# Method to query the database based on text in the entry fields
def getQuery():
    results = []
    query_list = []
    for e in entry_list:
        if e.get()=="":
            query_list.append("%" + str(e.get()) + "%")
        else:
            if e == entry_list[6] or e == entry_list[5] or e == entry_list[9]:
                query_list.append("%" + str(e.get()) + "%")
            else:
                query_list.append(str(e.get()))

    # Executes query amognst table
    thequery=cur.execute('''SELECT DISTINCT * FROM Movie natural join
(select movie_id from Actor natural join Acts where actor_last_name LIKE ?)
natural join (select movie_id from Genre natural join MovieGenre where genre_type LIKE ?)
natural join (select movie_id from Writer natural join Writes where last_name LIKE ?)
natural join (select movie_id from Director natural join Directs where director_last_name LIKE ?)
natural join Award
where oscar LIKE ? AND plot LIKE ? AND title LIKE ? AND rated LIKE ? AND imdbRating LIKE ? AND release_date LIKE ?
''',(query_list[0],query_list[1],query_list[2],query_list[3],query_list[4],query_list[5],query_list[6],
     query_list[7],query_list[8],query_list[9],))

    # Fetches all responses, deletes items in the tree, and then recreates the tree based on query
    fetch = thequery.fetchall()
    for x in fetch:
        results.append(x)
    tree.delete(*tree.get_children())
    for r in results:
        tree.insert('', 'end', values=r)
    clearFields()

# Method to insert movie into the database, user can input data but
# upon application close, movie will be correctly updated by the API
def insertMovie():
    results = []
    # Retrieves data from entry fields
    title = str(movie_title_entry.get())
    plot = str(plot_entry.get())
    rated = str(rated_entry.get())
    release_date = str(release_date_entry.get())
    imdbRating = str(imdb_rating_entry.get())

    entry_list.insert(6, title)
    entry_list.insert(5, plot)
    entry_list.insert(7, rated)
    entry_list.insert(9, release_date)
    entry_list.insert(8, imdbRating)

    # Writes to the file the new movie title, and inserts the data into the DB
    movie_file = open("movie_samples.data", "a")
    movie_file.write(title + '\n')
    print title, 'inserted successfully!'
    insert = cur.execute('''INSERT OR IGNORE INTO Movie (title, plot, runtime, rated, release_date, imdbID, imdbVotes, imdbRating, metascore)
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? )''', (title, plot,'', rated, release_date,'','',imdbRating,'' ) )
    conn.commit()
    movie_file.close()

    # Reopens the file to be read only and updates the tree to account for new entry
    new_movie_file = open("movie_samples.data", "r")
    fetch = cur.execute("SELECT * FROM Movie").fetchall()
    for movie in fetch:
        results.append(movie)
    columns = [column[0] for column in cur.description]
    createTree(columns, results)
    clearFields()
    new_movie_file.close()

# Method to delete movie, where user can delete movie from DB using the movie title
def deleteMovie():
    results = []

    # Retrieves data from movie title entry field
    movie_title = str(movie_title_entry.get())

    # Opens the file to be read only and stores the data in lines
    movie_file = open("movie_samples.data", "r")
    lines = movie_file.readlines()
    movie_file.close()

    # Reopens file to be written, deleted, and recreated not accounting for the movie to be deleted
    new_movie_file = open("movie_samples.data", "a")
    new_movie_file.seek(0)
    new_movie_file.truncate()
    for l in lines:
        if l!= movie_title + '\n':
            new_movie_file.write(l)
    delete = cur.execute('''DELETE FROM Movie WHERE title = ?''', (movie_title,))
    new_movie_file.close()
    conn.commit()

    # Fetches the updated DB and recreates the tree
    fetch = cur.execute("SELECT * FROM Movie").fetchall()
    for movie in fetch:
        results.append(movie)
    columns = [column[0] for column in cur.description]
    createTree(columns, results)
    print movie_title, 'deleted successfully!'
    clearFields()

# Method to create the labels for the entry fields
def createVerticalLabels():
    r = 1
    for l in y_labels:
        label = Label(BottomFrame, text=l, relief=FLAT, width=25)
        label.grid(row=r, column=0)
        r = r+1

#Create entries for labels
movie_title_entry = Entry(BottomFrame, bg='white',relief=SUNKEN,width=25)
movie_title_entry.grid(row=1, column=1)
actor_entry = Entry(BottomFrame, bg='white',relief=SUNKEN,width=25)
actor_entry.grid(row=2, column=1)
genre_entry = Entry(BottomFrame, bg='white',relief=SUNKEN,width=25)
genre_entry.grid(row=3, column=1)
director_entry = Entry(BottomFrame, bg='white',relief=SUNKEN,width=25)
director_entry.grid(row=4, column=1)
plot_entry = Entry(BottomFrame, bg='white',relief=SUNKEN,width=25)
plot_entry.grid(row=5, column=1)
release_date_entry = Entry(BottomFrame, bg='white',relief=SUNKEN,width=25)
release_date_entry.grid(row=6, column=1)
rated_entry = Entry(BottomFrame, bg='white',relief=SUNKEN,width=25)
rated_entry.grid(row=7, column=1)
imdb_rating_entry = Entry(BottomFrame, bg='white',relief=SUNKEN,width=25)
imdb_rating_entry.grid(row=8, column=1)
writer_entry = Entry(BottomFrame, bg='white',relief=SUNKEN,width=25)
writer_entry.grid(row=9, column=1)
oscars_entry = Entry(BottomFrame, bg='white',relief=SUNKEN,width=25)
oscars_entry.grid(row=10, column=1)

entry_list = [actor_entry,genre_entry,writer_entry,director_entry,oscars_entry,plot_entry,movie_title_entry
              ,rated_entry,imdb_rating_entry,
               release_date_entry]

# Creation of the insert & delete buttons
insert_button = Button(BottomFrame, text="Insert",  command=insertMovie)
insert_button.grid(row=11, column=1)
delete_button = Button(BottomFrame, text="Delete", command=deleteMovie)
delete_button.grid(row=11, column=2)

# Create the search button
SearchButton = Button(BottomFrame, text="Search",command=getQuery)
SearchButton.grid(row=11, column=0)

# Call methods to create the tree and the labels
createTree(columns, results)
createVerticalLabels()

# Help labels to instruct the user how to operate the GUI
helpTitle = Label(BottomFrame, text="Help Section", font=("Helvetica", 25))
helpTitle.grid(row=2, column=5)
helpLabel = Label(BottomFrame, text="- Search:  Loads up entire database when table empty", relief=FLAT, width=55)
helpLabel.grid(row=3, column=5)
helpLabel2 = Label(BottomFrame, text="- Delete:  Can only delete movies by entering movie title", relief=FLAT, width=55)
helpLabel2.grid(row=4, column=5)
helpLabel3 = Label(BottomFrame, text="- Insert:  Whatever information is left blank will be loaded in by the API the next time the window loads", relief=FLAT, width=105)
helpLabel3.grid(row=5, column=5)

root.mainloop()

# Close connections
cur.close()
conn.commit()
conn.close()
