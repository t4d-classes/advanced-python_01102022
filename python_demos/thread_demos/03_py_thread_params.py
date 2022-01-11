""" py thread """

import time
import threading


def do_it(msg1: str, msg2: str) -> None:
    """ do it """

    # time.sleep(1)

    print("did it: ", msg1, msg2)

print("start main thread")

thread1 = threading.Thread(target=do_it, args=("thread1", "software is cool"))
thread1.start()

thread2 = threading.Thread(target=do_it, args=("thread2", "programming is fun"))
thread2.start()

print("end main thread")
