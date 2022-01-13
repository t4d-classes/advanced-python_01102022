from typing import Any
from contextlib import closing
import pathlib
import math
import csv

import yaml
import pymongo


def read_config() -> Any:
    """ read config """

    with open(pathlib.Path("rates_demo", "config", "rates_config.yaml")) as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.SafeLoader)

config = read_config()

conn_string = f"mongodb://{config['database']['username']}:" \
            f"{config['database']['password']}@" \
            f"{config['database']['host']}:" \
            f"{config['database']['port']}"

with closing(pymongo.MongoClient(conn_string)) as client:

    db = client[config['database']['name']]
    rates_col = db["rates"]

    rates_file_path = pathlib.Path("..", "data", "eurofxref-hist.csv")

    with open(rates_file_path) as rates_file:

        rates_file_csv = csv.DictReader(rates_file)

        for rate_row in rates_file_csv:
            rate_entry = { "Date": rate_row["Date"], "EUR": 1.0 }

            for rate_col in rate_row:
                if rate_col != "Date" and len(rate_col) > 0:
                    if rate_row[rate_col] == "N/A":
                        rate_entry[rate_col] = math.nan
                    else:
                        rate_entry[rate_col] = float(rate_row[rate_col])

            rates_col.insert_one(rate_entry)

