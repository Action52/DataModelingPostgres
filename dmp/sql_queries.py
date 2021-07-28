# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS song"
artist_table_drop = "DROP TABLE IF EXISTS artist"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays 
        (
            songplay_id SERIAL NOT NULL, 
            start_time  VARCHAR,
            user_id     INTEGER, 
            level       VARCHAR, 
            song_id     VARCHAR, 
            artist_id   VARCHAR, 
            session_id  INTEGER, 
            location    VARCHAR,
            user_agent  VARCHAR,
            PRIMARY KEY (songplay_id),
            FOREIGN KEY(user_id) 
                REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY(song_id) 
                REFERENCES song(song_id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY(artist_id) 
                REFERENCES artist(artist_id) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY(start_time) 
                REFERENCES time(start_time) ON UPDATE CASCADE ON DELETE CASCADE
        )""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users 
        (
            user_id     INTEGER UNIQUE NOT NULL, 
            first_name  VARCHAR, 
            last_name   VARCHAR,
            gender      VARCHAR, 
            level       VARCHAR,
            PRIMARY KEY (user_id)
        )""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS song 
        (
            song_id     VARCHAR NOT NULL, 
            title       VARCHAR, 
            artist_id   VARCHAR, 
            year        INTEGER,
            duration    FLOAT,
            PRIMARY KEY(song_id)
        )""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artist 
        (
            artist_id   VARCHAR UNIQUE NOT NULL, 
            name        VARCHAR, 
            location    VARCHAR,
            latitude    FLOAT, 
            longitude   FLOAT,
            PRIMARY KEY(artist_id)
        )""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time 
        (
            start_time  VARCHAR NOT NULL, 
            hour        VARCHAR, 
            day         VARCHAR, 
            week        VARCHAR,
            month       VARCHAR, 
            year        VARCHAR, 
            weekday     VARCHAR,
            PRIMARY KEY (start_time)
        )""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays 
        (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""")

user_table_insert = ("""
    INSERT INTO users 
        (user_id, first_name, last_name, gender, level)
    VALUES (%s, %s, %s, %s, %s) 
    ON CONFLICT (user_id) DO 
        UPDATE SET 
            level=EXCLUDED.level""")

song_table_insert = ("""
    INSERT INTO song
        (song_id, title, artist_id, year, duration)
    VALUES (%s, %s, %s, %s, %s) 
    ON CONFLICT(song_id) DO NOTHING
    """)

time_table_insert = ("""
    INSERT INTO time 
        (start_time, hour, day, week, month, year, weekday) 
    VALUES (%s, %s, %s, %s, %s, %s, %s) 
    ON CONFLICT(start_time) DO NOTHING""")

artist_table_insert = ("""
    INSERT INTO artist 
        (artist_id, name, location, latitude, longitude)
    VALUES (%s, %s, %s, %s, %s) 
    ON CONFLICT(artist_id) DO NOTHING""")

# FIND SONGS

song_select = ("""
    SELECT 
        song_id, artist.artist_id 
    FROM 
        (song JOIN artist ON artist.artist_id = song.artist_id)
    WHERE 
        song.title = %s AND 
        artist.name = %s AND 
        song.duration = %s""")

# QUERY LISTS

create_table_queries = [user_table_create, artist_table_create, song_table_create, time_table_create,
                        songplay_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]