import asyncio
from random import randint
import threading
import time
import aiofiles
from datetime import datetime

def delay():
    """ delay """
    return randint(1,10) / 2

def get_data_sync(task_num: int) -> None:
    """ get data """
    print(f"thread id: {threading.get_ident()}, task: {task_num}, starting get data")
    
    with open("data.txt", encoding="UTF-8") as f:
        print(f"thread id: {threading.get_ident()}, task: {task_num}", f.readlines())

    print(f"thread id: {threading.get_ident()}, task: {task_num}, finished get data")


async def get_data_async(task_num: int) -> None:
    """ get data """
    print(f"thread id: {threading.get_ident()}, task: {task_num}, starting get data")

    # read a file synchronously
    # with open("data.txt", encoding="UTF-8") as f:
    #     print(f"thread id: {threading.get_ident()}, task: {task_num}", f.readlines())

    async with aiofiles.open("data.txt", encoding="UTF-8") as f:
        print(f"thread id: {threading.get_ident()}, task: {task_num}", await f.readlines())

    print(f"thread id: {threading.get_ident()}, task: {task_num}, finished get data")



async def main():

    start_time = datetime.now()

    get_data_sync(1)
    get_data_sync(2)
    get_data_sync(3)

    print(datetime.now() - start_time)

    # await asyncio.gather(
    #     asyncio.to_thread(get_data_sync, 1),
    #     asyncio.to_thread(get_data_sync, 2),
    #     asyncio.to_thread(get_data_sync, 3),
    # )

    start_time = datetime.now()

    task1 = asyncio.create_task(get_data_async(1))
    task2 = asyncio.create_task(get_data_async(2))
    task3 = asyncio.create_task(get_data_async(3))

    await task1
    await task2
    await task3

    print(datetime.now() - start_time)

asyncio.run(main())