""" date format demo """

from datetime import date, datetime

independence_day = date(1776, 7, 4)

print(independence_day)
print(type(independence_day))

print(datetime.now())
print(type(datetime.now()))

print(datetime.now().strftime("%B %A"))


TAX_DAY_STR = "05-2021-17"

tax_day = datetime.strptime(TAX_DAY_STR, "%m-%Y-%d")
print(tax_day)
