""" rates api """

from typing import Any
from contextlib import closing
import pathlib
import math

from flask import Flask, jsonify, abort, request, Response
import yaml
import pymongo


def read_config() -> Any:
    """ read config """

    with open(pathlib.Path(
        "rates_demo", "config", "rates_config.yaml")) as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.SafeLoader)

config = read_config()

conn_string = f"mongodb://{config['database']['username']}:" \
            f"{config['database']['password']}@" \
            f"{config['database']['host']}:" \
            f"{config['database']['port']}"

rates: list[dict[str,Any]] = []

app = Flask(__name__)

@app.route("/check")
def check() -> str:
    """ health check route function """
    return "READY"


@app.route("/api/<rate_date>")
def rates_by_date(rate_date: str) -> Response:

    with closing(pymongo.MongoClient(conn_string)) as client:

        db = client[config['database']['name']]
        rates = list(db["rates"].find({ "Date": rate_date }))

        if len(rates) == 0:
            abort(404)
            return

        rate = rates[0]

        base_country = request.args.get("base", "EUR")

        if "symbols" in request.args:
            country_symbols = request.args["symbols"].split(",")
        else:
            country_symbols = [col for col in rate if col != "Date"]

        country_rates = {
            country_code: country_rate / rate[base_country]
            for (country_code, country_rate) in rate.items()
            if country_code in country_symbols and
            not math.isnan(country_rate)
        }

        return jsonify({
            "date": rate["Date"],
            "base": base_country,
            "rates": country_rates
        })


def start_rates_api() -> None:
    """ start rates api rest server """

    app.run()

if __name__ == "__main__":
    start_rates_api()
