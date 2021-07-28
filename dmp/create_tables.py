import psycopg2
import pandas as pd
import psycopg2.extras as extras

class PostgresConnector:
    def __init__(self, host="localhost", port=5432, user=None, password=None, dbname=None):
        try:
            self.host = host
            self.port = port
            self.user = user
            self.password = password
            self.dbname = dbname
            self.conn = psycopg2.connect(f"host={self.host} port={self.port} dbname={self.dbname} "
                                         f"user={self.user} password={self.password}")
            self.conn.set_session(autocommit=True)
            self.cur = self.conn.cursor()

        except psycopg2.Error as e:
            print(e)
            print("Something wrong happened when connecting.")

    def close(self):
        self.conn.close()

    def get_conn(self):
        return self.conn

    def get_cur(self):
        return self.cur

    def create_db(self, dbname=None):
        try:
            if dbname is not None:
                self.get_cur().execute(f"DROP DATABASE IF EXISTS {dbname}")
                self.get_cur().execute(f"CREATE DATABASE {dbname} WITH ENCODING 'utf-8' TEMPLATE template0")
            else:
                print("dbname cannot be None.")
        except psycopg2.Error as e:
            print(e)
            print("Something happened when creating the db.")

    def drop_tables(self, queries):
        for query in queries:
            try:
                self.get_cur().execute(query)
                print(f"Successfully dropped table.")
            except psycopg2.Error as e:
                print(e)
                print(f"Error when dropping table. Try again.")

    def create_tables(self, queries):
        for query in queries:
            try:
                self.get_cur().execute(query)
                print(f"Successfully created table.")
            except psycopg2.Error as e:
                print(e)
                print(query)
                print(f"Error when creating table. Try again.")

    def insert_data(self, query, df: pd.DataFrame):
        try:
            actual = None
            if self.get_conn().autocommit is True:
                self.get_conn().set_session(autocommit = False)
            data_load = [list(row) for row in df.to_numpy()]
            # for data in data_load:
            #     actual = data
            #     # print(actual)
            #     self.get_cur().execute(query, data)
            self.get_cur().executemany(query, data_load)
            self.get_conn().commit()
            self.get_conn().set_session(autocommit=True)
            # print("Data inserted correctly.")
        except psycopg2.Error as e:
            print(actual)
            self.get_conn().rollback()
            self.get_conn().set_session(autocommit = True)
            print(e)
            print("Error when inserting data. Rolling back.")