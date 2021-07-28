from dmp import PostgresConnector
import pandas as pd
import os
from tqdm import tqdm
from dmp.sql_queries import *
import datetime
import psycopg2
from argparse import ArgumentParser


def load_data_from_json(df, path):
    return df.append(pd.read_json(path, lines=True))


def load_dataset(df, path):
    for(path, dirnames, filenames) in os.walk(path):
        filepaths = [filename for filename in filenames if ".json" in filename]
        if filepaths:
            for filepath in filepaths:
                df = load_data_from_json(df, path+"/"+filepath)
    return df


def query_song(pc: PostgresConnector, query, data):
    try:
        pc.get_cur().execute(query, data)
        results = pc.get_cur().fetchone()
        if results:
            return results
        else:
            return None, None
    except psycopg2.Error as e:
        print(e)


def main():
    parser = ArgumentParser()
    parser.add_argument("--songs-folder", required=True,
                        help="Path to the folder were all the song jsons are contained.")
    parser.add_argument("--logs-folder", required=True,
                        help="Path to the folder were all the log jsons are contained.")
    parser.add_argument("-r", "--reset-db", action="store_true",
                        help="If passed, the db's tables will be dropped and recreated.")
    parser.add_argument("-H", "--host", default="127.0.0.1", help="Host ip for the db.")
    parser.add_argument("-p", "--port", default=5432, help="Port for the db.", type=int)
    parser.add_argument("-U", "--user", help="User for the db.", required=True)
    parser.add_argument("-P", "--password", required=True, help="Password for the db.")
    parser.add_argument("-d", "--db-name", default="sparkify", help="Name of the db.")
    args = parser.parse_args()

    # Create the connector to the db
    pc = PostgresConnector(host=args.host, port=args.port, user=args.user, password=args.password, dbname=args.db_name)

    # Recreate the db if stated
    if args.reset_db:
        pc.drop_tables(drop_table_queries)
        pc.create_tables(create_table_queries)

    # Load the general dfs
    df_songs = pd.DataFrame()
    df_logs = pd.DataFrame()
    df_songs = load_dataset(df=df_songs, path=args.songs_folder)
    df_logs = load_dataset(df=df_logs, path=args.logs_folder)
    df_logs.loc[:, "userId"] = df_logs["userId"].replace("", -1).astype(int)

    # Create the artist DataFrame with which we will populate the artist psql table.
    artist_data = df_songs[["artist_id", "artist_name", "artist_location", "artist_latitude", "artist_longitude"]].copy(deep=True)
    artist_data.reset_index(inplace=True, drop=True)
    artist_data.drop_duplicates(subset="artist_id", inplace=True)

    # Create the songs DataFrame with which we will populate the songs psql table.
    songs_data = df_songs[["song_id", "title", "artist_id", "year", "duration"]].copy(deep=True)
    songs_data.reset_index(inplace=True, drop=True)

    # Create the user DataFrame with which we will populate the users psql table.
    user_data = df_logs[["userId", "firstName", "lastName", "gender", "level"]].copy(deep=True)
    user_data.loc[:, "userId"] = pd.to_numeric(user_data["userId"], downcast="integer")
    user_data.drop_duplicates("userId", inplace=True)
    user_data.dropna(inplace=True, subset=["userId"])
    user_data = user_data[user_data["userId"] != ""]
    user_data.reset_index(inplace=True, drop=True)

    # Create the times DataFrame with which we will populate the times psql table.
    time_data = df_logs[["ts"]].copy(deep=True)
    time_data.drop_duplicates("ts", inplace=True)
    time_data.loc[:, "start_time"] = time_data["ts"].astype(str)
    time_data.loc[:, "ts"] = time_data["ts"].apply(lambda x: datetime.datetime.fromtimestamp(x / 1000))
    time_data.loc[:, "hour"] = pd.DatetimeIndex(time_data["ts"]).hour
    time_data.loc[:, "day"] = pd.DatetimeIndex(time_data["ts"]).day
    # time_data["week"] = pd.DatetimeIndex(time_data["ts"]).weekofyear
    time_data.loc[:, "week"] = time_data["ts"].dt.isocalendar().week
    time_data.loc[:, "month"] = pd.DatetimeIndex(time_data["ts"]).month
    time_data.loc[:, "year"] = pd.DatetimeIndex(time_data["ts"]).year
    time_data.loc[:, "weekday"] = pd.DatetimeIndex(time_data["ts"]).weekday
    time_data.drop(columns="ts", inplace=True)

    # Populate the dimension tables
    print("Inserting data into the fact tables.")
    pc.insert_data(song_table_insert, songs_data)
    pc.insert_data(artist_table_insert, artist_data)
    pc.insert_data(user_table_insert, user_data)
    pc.insert_data(time_table_insert, time_data)

    # Now we are able to create the songplays fact table
    print("Inserting data into the songplays table.")
    rows = []
    for index, row in tqdm(df_logs.iterrows(), total=df_logs.shape[0]):
        song_id, artist_id = query_song(pc, song_select, (row["song"], row["artist"], row["length"]))
        rows.append({"start_time": row["ts"], "user_id": row["userId"], "level": row["level"],
                     "song_id": song_id, "artist_id": artist_id, "session_id": row["sessionId"],
                     "location": row["location"], "user_agent": row["userAgent"]})
    songplay_data = pd.DataFrame(rows)
    pc.insert_data(songplay_table_insert, songplay_data)


if __name__ == "__main__":
    main()