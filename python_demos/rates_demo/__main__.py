""" main """

import requests
from rates_demo.get_rates import get_rates, get_rates_threaded
from rates_demo.rates_api_server import rates_api_server
import time

if __name__ == "__main__":

    with rates_api_server():

        print("server started")

        # time.sleep(5)

        # requests.get('http://127.0.0.1:5000/check').text

        get_rates_threaded()
