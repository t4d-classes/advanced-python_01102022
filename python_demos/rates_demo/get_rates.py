""" get rates """

from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta
import requests
import threading

from rates_demo.business_days import business_days

def get_rates() -> None:
    """ get rates """

    start_date = date(2021, 1, 1)
    end_date = start_date + timedelta(days=20)

    rate_responses: list[str] = []

    for business_day in business_days(start_date, end_date):

        rate_url = "".join([
            "http://127.0.0.1:5000/api/",
            str(business_day),
            "?base=USD&symbols=EUR"
        ])

        response = requests.get(rate_url)
        rate_responses.append(response.text)

    
    for rate_response in rate_responses:
        print(rate_response)

def get_rate_task(business_day: date, responses: list[str]) -> str:
    """ get rate from rates api """

    rate_url = "".join([
        "http://127.0.0.1:5000/api/",
        str(business_day),
        "?base=USD&symbols=EUR"
    ])

    response = requests.get(rate_url)
    responses.append(response.text)


def get_rates_threaded() -> None:
    """ get rates using threads """

    start_date = date(2021, 1, 1)
    end_date = start_date + timedelta(days=20)

    rate_responses: list[str] = []
    threads: list[threading.Thread] = []

    for business_day in business_days(start_date, end_date):
        a_thread = threading.Thread(
            target=get_rate_task, args=(business_day,rate_responses))
        a_thread.start()
        threads.append(a_thread)

    for a_thread in threads:
        a_thread.join()    

    for rate_response in rate_responses:
        print(rate_response)


def get_rate_task_for_pool(business_day: date) -> str:
    """ get rate from rates api """

    rate_url = "".join([
        "http://127.0.0.1:5000/api/",
        str(business_day),
        "?base=USD&symbols=EUR"
    ])

    response = requests.get(rate_url)
    return response.text


def get_rates_threadpool() -> None:
    """ get rates using threads """

    start_date = date(2021, 1, 1)
    end_date = start_date + timedelta(days=20)

    rate_responses: list[str] = []

    with ThreadPoolExecutor() as executor:
        rate_responses = list(executor.map(
            get_rate_task_for_pool,
            [ business_day for business_day
            in business_days(start_date, end_date) ]
        ))


    for rate_response in rate_responses:
        print(rate_response)                


if __name__ == "__main__":
    # get_rates()
    get_rates_threaded()
    # get_rates_threadpool()
    