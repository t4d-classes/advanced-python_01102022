""" business days module """

from datetime import date, timedelta
from collections.abc import Generator
import holidays

def business_days_list(sdate: date, edate: date) -> list[date]:
    """ get business between the start date and end date inclusive """

    days: list[date] = []

    us_holidays = holidays.UnitedStates()

    num_of_days = (edate - sdate).days + 1

    for num in range(num_of_days):
        the_date = sdate + timedelta(days=num)
        if (the_date.weekday() < 5) and (the_date not in us_holidays):
            days.append(the_date)

    return days

def business_days(sdate: date, edate: date) -> Generator[date, None, None]:
    """ get business between the start date and end date inclusive """

    us_holidays = holidays.UnitedStates()

    num_of_days = (edate - sdate).days + 1

    for num in range(num_of_days):
        the_date = sdate + timedelta(days=num)
        if (the_date.weekday() < 5) and (the_date not in us_holidays):
            yield the_date


if __name__ == "__main__":

    start_date = date(2020, 1, 1)
    end_date = date(2020, 2, 29)

    for business_day in business_days_list(start_date, end_date):
        print(business_day)
