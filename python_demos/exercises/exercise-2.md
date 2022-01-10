
# Exercise 2

1. Implement this code in `__main__.py` in the `rates_demo` folder. Move the Rates REST API code from the last demo into a new file named `rates_api.py`.

2. Install the "requests" package from PyPi.org. (We did this already)

https://docs.python-requests.org/en/master/user/quickstart/#make-a-request

3. Using the "requests" package API, call the following URL for each date returned from the "business_days" function.

http://127.0.0.1:5000/api/2019-01-01?base=USD&symbols=EUR

Iterate over a range of 20 days, and run the above request for each business day.

4. Create a list of text values from each response. The text value is formatted as JSON. Do not parse the JSON. Just put each JSON response in the list.

5. Display each list item in the console.