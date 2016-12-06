from Tkinter import *
import ttk
from FillDatabase import *
import sqlite3

root = Tk()
# width x height + x_offset + y_offset (+30 each but i removed)
root.geometry("1170x700")

y_labels = ['Movie Title:', 'Actor:', 'Genre:', 'Director:', 'Plot:', 'Release Date:', 'Rated:', 'IMDb Rating:', 'Writer:', 'Oscars:']
x_labels = ['Insert', 'Delete']

title = Label(root, text="Movies Database", font=("Helvetica", 25))
title.grid(row=0, column=1)
tree = NoneType

MidFrame = Frame(root, bg="white", height=100, width=500)
MidFrame.pack(side=LEFT, expand=1)
MidFrame.grid(row=13, column=1)

BottomFrame = Frame(root, bg="white", height=500, width=500)
BottomFrame.pack(side=LEFT, expand=1)
BottomFrame.grid(row=15, column=1)

def createTree(column, data):
    global tree

    if tree != NoneType:
        tree.destroy()

    tree = ttk.Treeview(columns=column, show='headings')
    tree.pack(expand=YES, fill=BOTH)
    for c in column:
        tree.heading(c, text=c.title())
        tree.column(c, width=115, stretch=True)

    for d in data:
        tree.insert('', 'end', values=d)

    y_scroll = ttk.Scrollbar(orient=VERTICAL, command=tree.yview)
    x_scroll = ttk.Scrollbar(orient=HORIZONTAL, command=tree.xview)
    tree['yscroll'] = y_scroll.set
    tree['xscroll'] = x_scroll.set

    tree.grid(row=5, column=1, columnspan=100, sticky=W, padx=10)

def insertMovie():
    results = []
    movie = str(insert_entry.get())
    movie_file = open("movie_samples.data", "a")
    movie_file.write(movie + '\n')
    # populateDB()
    print movie, 'inserted successfully!'
    insert = cur.execute('''INSERT OR IGNORE INTO Movie (title, plot, runtime, rated, release_date, imdbID, imdbVotes, imdbRating, metascore)
            VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ? )''', (buffer(movie),'','','','','','','','' ) )
    fetch = insert.fetchall()
    for f in fetch:
        results.append(f)
    for r in results:
        tree.insert('', 'end', values=r)


def deleteMovie():
    results = []
    movie = str(delete_entry.get())
    movie_file = open("movie_samples.data", "r")
    lines = movie_file.readlines()
    movie_file.close()
    new_movie_file = open("movie_samples.data", "a")
    new_movie_file.seek(0)
    new_movie_file.truncate()
    for l in lines:
        if l!= movie + '\n':
            new_movie_file.write(l)
    new_movie_file.close()
    print movie, 'deleted successfully!'

def createVerticalLabels():
    r = 1
    for l in y_labels:
        label = Label(BottomFrame, text=l, relief=FLAT, width=15)
        label.grid(row=r, column=0)
        r = r+1

#Create Entries for Labels
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

insert_label = Label(MidFrame, text="Insert Movie: ").grid(row=0, column=1)
insert_entry = Entry(MidFrame, bg='white',relief=SUNKEN,width=25)
insert_entry.grid(row=0, column=2)
insert_button = Button(MidFrame, text="Insert",  command=insertMovie)
insert_button.grid(row=0, column=3)
delete_label = Label(MidFrame, text="Delete Movie: ").grid(row=0, column=4)
delete_entry = Entry(MidFrame, bg='white',relief=SUNKEN,width=25)
delete_entry.grid(row=0, column=5)
delete_button = Button(MidFrame, text="Delete", command=deleteMovie)
delete_button.grid(row=0, column=6, padx=10)

conn = sqlite3.connect('moviedata.sqlite')
cur = conn.cursor()
fetch = cur.execute("SELECT * FROM Movie").fetchall()
columns = [column[0] for column in cur.description]
results = []

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

    thequery=cur.execute('''SELECT DISTINCT * FROM Movie natural join
(select movie_id from Actor natural join Acts where actor_last_name LIKE ?)
natural join (select movie_id from Genre natural join MovieGenre where genre_type LIKE ?)
natural join (select movie_id from Writer natural join Writes where last_name LIKE ?)
natural join (select movie_id from Director natural join Directs where director_last_name LIKE ?)
natural join Award
where oscar LIKE ? AND plot LIKE ? AND title LIKE ? AND rated LIKE ? AND imdbRating LIKE ? AND release_date LIKE ?
''',(query_list[0],query_list[1],query_list[2],query_list[3],query_list[4],query_list[5],query_list[6],
     query_list[7],query_list[8],query_list[9],))
    fetch = thequery.fetchall()
    for x in fetch:
        results.append(x)
    tree.delete(*tree.get_children())
    for r in results:
        tree.insert('', 'end', values=r)

SearchButton = Button(BottomFrame, text="Search",command=getQuery)
SearchButton.grid(row=11, column=1)
createTree(columns, results)

createVerticalLabels()
# fillHorizontal()
root.mainloop()
