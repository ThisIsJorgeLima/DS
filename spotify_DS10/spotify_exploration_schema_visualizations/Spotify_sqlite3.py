import sqlite3

conn = sqlite3.connect('spotify.db')
c = conn.cursor()

c.execute("""CREATE TABLE artist_name (
            first text,
            track_id  integer,
            track_name text,
            acousticness real,
            danceability real,
            duration_ms integer,
            energy real,
            instrumentalness real,
            key integer,
            liveness real,
            loudness real,
            mode integer,
            speechiness real,
            tempo real,
            time_signature integer,
            valence real,
            popularity integer
            )""")
c.execute("INSERT INTO employees ")
conn.commit()
conn.close()
