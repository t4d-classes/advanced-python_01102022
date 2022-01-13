from tasks import echo, get_list, create_person
from time import sleep
from celery import group

# result = echo.delay("hello")
# result = get_list.delay(4, 8)
# result = create_person.delay('Bob', 'Smith')

fn = group([ get_list.s(i, i) for i in range(4) ])
result = fn()

print("checking")
while not result.ready():
    sleep(5)
    print("checking")

print(result.get())