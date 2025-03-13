from os import environ

import sqlite3
import pandas as pd

DB_NAME = environ.get('DB_NAME')


def save_to_db(df: pd.DataFrame):
    with sqlite3.connect(DB_NAME) as conn:
        df.to_sql('sites', conn, if_exists='append', index=False)
