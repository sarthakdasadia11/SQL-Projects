# Import XML tree and sqlite3

import xml.etree.ElementTree as ET
import sqlite3

conn = sqlite3.connect('trackdb.sqlite')
cur = conn.cursor() # cursor object for SQL


# Create SQL table: Artist, Genre, Album, Track

cur.executescript('''
    
    DROP TABLE IF EXISTS Artist;
    DROP TABLE IF EXISTS Genre;
    DROP TABLE IF EXISTS Album;
    DROP TABLE IF EXISTS Track;
    
    CREATE TABLE Artist (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
    );
    
    CREATE TABLE Genre (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name    TEXT UNIQUE
    );
    
    CREATE TABLE Album (
    id  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id  INTEGER,
    title   TEXT UNIQUE
    );
    
    CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY
    AUTOINCREMENT UNIQUE,
    title TEXT  UNIQUE,
    album_id  INTEGER,
    genre_id  INTEGER,
    len INTEGER, rating INTEGER, count INTEGER
    );
    
    ''')

# Import the XML file / parse it

fname = 'Library.xml'

stuff = ET.parse(fname)

lst = stuff.findall('dict/dict/dict')
print 'User count:', len(lst)

# find function gets the value for required key. e.g., the itunes music library has following code:
# <key>Track ID</key><integer>369</integer>
# <key>Name</key><string>Another One Bites The Dust</string>
# <key>Artist</key><string>Queen</string>


def find(d, key):
    found = False
    for entry in d:
        if found : return entry.text
        if entry.tag == 'key' and entry.text == key :
            found = True  # go to next tag and get the value
    return None



for item in lst:
    #print 'Name', find(item, 'Name')  -- CHECK
    name = find(item, 'Name')
    #print 'Artist', find(item, 'Artist')  -- CHECK
    artist = find(item, 'Artist')
    album = find(item, 'Album')
    count = find(item, 'Play Count')
    rating = find(item, 'Rating')
    length = find(item, 'Total Time')
    genre = find(item, 'Genre')
    
    if name is None or artist is None or album is None :
        continue

    print name, artist, album, genre, count, rating, length


# So We have all the data extracted from the XML file. Now, add data into the databse.

    cur.execute('''INSERT OR IGNORE INTO Artist (name) VALUES ( ? )''', ( artist, ) )
    cur.execute('SELECT id FROM Artist WHERE name = ? ', (artist, ))
    artist_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Album (title, artist_id) VALUES ( ?, ? )''', ( album, artist_id ) )
    cur.execute('SELECT id FROM Album WHERE title = ? ', (album, ))
    album_id = cur.fetchone()[0]

    cur.execute('''INSERT OR IGNORE INTO Genre (name) VALUES ( ?)''', ( genre, ) )
    cur.execute('SELECT id FROM Genre WHERE name = ? ', (genre, ))
    genre_id = cur.fetchone()[0]

    cur.execute('''INSERT OR REPLACE INTO Track (title, album_id, genre_id, len, rating, count) VALUES ( ?, ?, ?, ?, ?, ? )''',( name, album_id, genre_id, length, rating, count ) )

    conn.commit()




