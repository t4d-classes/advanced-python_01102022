""" time delta demo """

from datetime import datetime, timedelta
import time


start = datetime.now()

end = start + timedelta(days=20)

print(start)
print(end)

start = datetime.now()

time.sleep(2)

end = datetime.now()

print(end - start)
print(type(end - start))