""" py thread """

import time
import threading


def do_it(id: str) -> None:
    """ do it """

    # time.sleep(1)

    print("did it: " + id)

print("start main thread")

thread1 = threading.Thread(target=do_it, args=("1", ))
thread1.start()

thread2 = threading.Thread(target=do_it, args=("2", ))
thread2.start()

print("end main thread")
