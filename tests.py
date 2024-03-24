# Load required libraries.
import numpy as np
import pandas as pd
from datetime import datetime
from datetime import timedelta
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
import json


# Specify database defaults
connection_params = json.load(
    open("/Users/callanroff/Desktop/Acc. Keyzzz/postgresql_conn_params.json", "r")
)
schema_name="web_scraping"
table_name="music_events"
input_venues = [
    "Brunswick Ballroom",
    "The Night Cat",
    "Croxton Bandroom",
    "Corner Hotel",
    "Northcote Theatre",
    "Northcote Social Club",
    "The Workers Club",
    "The Retreat",
    "Sub Club",
    "Miscellania",
    "Melbourne Recital Centre",
    "280 Sydney Rd",
    "Max Watt's Melbourne",
    "Sidney Myer Music Bowl",
    "Forum Melbourne",
    "Howler",
    "The Toff in Town"
]


# TEST 1
# Ensure the the number of distinct venues match in the input and output
def number_of_venue_tests(connection_params = connection_params, schema_name = schema_name, table_name = table_name):
    num_inputs = len(input_venues)
    conn = psycopg2.connect(
        host = connection_params["host"],
        database = connection_params["database"],
        user = connection_params["user"],
        password = connection_params["password"]
    )
    query = f"""
        SELECT DISTINCT
            "VENUE"
        FROM {schema_name}.{table_name}
    """
    output_venues = list(pd.read_sql_query(query, conn)["VENUE"].unique())
    conn.close()
    num_outputs = len(output_venues)
    if num_inputs == num_outputs:
        print("Wooohooo! At least one result for all venues was generated :)))")
    else:
        all_venues_df = pd.DataFrame(zip(
            input_venues,
            [input_venues[i] in output_venues for i in range(len(input_venues))]
        ), columns = ["VENUE", "IN_OUTPUT"])
        missing_venues = all_venues_df[all_venues_df["IN_OUTPUT"] == False]["VENUE"].unique()
        missing_venues_format = ', '.join(missing_venues)
        print(f"""Input venues with no output: \n{missing_venues_format}""")
