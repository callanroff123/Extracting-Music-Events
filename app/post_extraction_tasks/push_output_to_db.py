# Load libraries required for exportation to PostgreSQL database
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import json
from app import config


# Pushes music_events.csv into our web-scraped database
def to_postgresql(connection_params, schema_name, table_name):
    conn = psycopg2.connect(
        host = connection_params["host"],
        database = connection_params["database"],
        user = connection_params["user"],
        password = connection_params["password"]
    )
    engine = create_engine('postgresql://' + connection_params["user"] + ':' + connection_params["password"] + '@' + connection_params["host"] + ':5432/' + connection_params["database"])
    df = pd.read_csv(str(config.OUTPUT_PATH) + "/music_events.csv")
    df = df[["Title", "Date", "Venue", "Link"]]
    df = df.rename(columns = {
        "Title": "TITLE",
        "Date": "DATE",
        "Venue": "VENUE",
        "Link": "LINK"
    })
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {schema_name}.{table_name}")
    cursor.execute(
        f'''
            CREATE TABLE {schema_name}.{table_name} (
                TITLE VARCHAR(1000),
                DATE DATE,
                VENUE VARCHAR(1000),
                LINK VARCHAR(1000)
            ); 
        '''
    )
    df.to_sql(
        table_name,
        engine,
        if_exists = "replace",
        schema = schema_name,
        index = False
    )
    conn.close()

# Run DB collection pipeline
def run_postgres_push():
    connection_params = json.load(
        open("/Users/callanroff/Desktop/Acc. Keyzzz/postgresql_conn_params.json", "r")
    )
    to_postgresql(
        connection_params = connection_params, 
        schema_name="web_scraping", 
        table_name="music_events"
    )