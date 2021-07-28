from dmp.sql_queries import *
from dmp.create_tables import *
from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument("-H", "--host", default="127.0.0.1", help="Host ip for the db.")
    parser.add_argument("-p", "--port", default=5432, help="Port for the db.", type=int)
    parser.add_argument("-U", "--user", help="User for the db.", required=True)
    parser.add_argument("-P", "--password", required=True, help="Password for the db.")
    parser.add_argument("-d", "--db-name", default="sparkify", help="Name of the db.")
    args = parser.parse_args()

    pc = PostgresConnector(host=args.host, port=args.port, user=args.user, password=args.password, dbname=args.db_name)
    pc.drop_tables(drop_table_queries)
    pc.create_tables(create_table_queries)


if __name__ == "__main__":
    main()