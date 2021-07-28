## Sparkify DB

Sparkify needs to correctly and efficiently store data related to the usage of their system.
Before, they used to store their data in two different sources, the first one containing a registry of songs and artists,
with the other containing a set of usage logs by Sparkify's users. This project implements a proposal to correctly save
this information into a relational schema, with all the advantages that this implies.

## Requirements
To run this project on your local machine you will need:
* Python >= 3.6
* Docker
* Conda or mini conda to install the environment.

### Installation

To install the repository as a Python package open a new terminal window, cd to the root of this project and execute the
following commands.

`conda create --name dmp python=3.6 --no-default-packages`  
`conda activate dmp`

This commands will create and start a clean conda environment to run the project.
Once we have set the environment, we can install the repo by simply doing, on the root of this repo:
`pip install -e .` This command executes the _setup.py_ script and installs the dependencies.

### Starting the Postgres service
This project works with a docker-compose.yml file. To start the service, type on the same terminal as before:
`docker-compose up -d`, which will start a containerized Postgres server while running on the background.
If you want to bring it down after using this repo, simply type `docker-compose down`.

### Running the etl.py script

To run the script that extract the jsons from the data/ folder and transforms it into our psql schema, simply do
`python scripts/etl.py`. These are the flags that can be sent to the script:  
* **--songs-folder** (**Required**): Path to the folder were all the song jsons are contained. I.e: `data/song_data/`.
* **--logs-folder** (**Required**): Path to the folder were all the log jsons are contained. I.e: `data/log_data/`
* **--reset-db** (a.k.a: **-r**): If passed, the Postgres db's tables will be dropped and recreated with the
code in dmp.create_tables.py.
* **--host** (a.k.a: **-H**): Host ip for the db Default is localhost.
* **--port** (a.k.a: **-p**): Port for the db. Default is 5432.
* **--user** (**Required**, a.k.a: **-U**): User for the db.
* **--password** (**Required**, a.k.a: **-P**): Password for the db.
* **--db-name**: Name of the database, default is "sparkify".
The user and password to run the project on the local psql service is: user `aleon` password `psqludacity`.

Example usage:
````
python scripts/etl.py --songs-folder data/song_data/ --logs-folder data/log_data/ \
    --user aleon --password psqludacity -r
````

This command will execute the etl.py script with the reset option activated.
The database will be created and populated with the songs and logs data.

The schema design is a classic Star datamart schema. It contains 4 dimension tables and 1 fact table.
#### Dimension tables
##### Song
This table represents the data related to the songs, such as the title, the artist_id, year and duration.
##### Artist
This table contains the data of the artists, like name, location, altitude and longitude.
##### Time
This table contains the reference for the timestamp on the logs. It is split into start_time, hour, day, week, month, year,
and weekday.
##### Users
This table contains the info of the users, like first name, last name, gender, and their level of subscription.

#### Fact Tables
##### Songplays
This fact table contains the keys for many dimension tables, such as user_id, song_id and artist_id, timestamp. Other
columns include location, session_id, and level.


The advantage of using this relational schema is that while we are sacrificing some write operations, we are able to quickly 
generate insights with our facts table, without having to perform any JOIN on the tables.


References

* https://www.arteco-consulting.com/instalar-postgresql-con-docker/
* https://www.programiz.com/python-programming/datetime/timestamp-datetime
* https://naysan.ca/2020/05/09/pandas-to-postgresql-using-psycopg2-bulk-insert-performance-benchmark/
* https://www.postgresqltutorial.com/postgresql-foreign-key/
