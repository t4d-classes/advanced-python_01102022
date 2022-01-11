""" thread local data """


import time
import threading

mydata = threading.local()

def python_is_fun():
    print("python is fun", mydata.msg)


def do_it(msg1: str, msg2: str) -> None:
    """ do it """

    print("did it: ", msg1, msg2)
    # print(mydata.msg)
    mydata.msg = msg1
    time.sleep(1)
    python_is_fun()

def do_it2(msg1: str, msg2: str) -> None:
    """ do it """

    print("did it: ", msg1, msg2)
    # print(mydata.msg)
    mydata.msg = msg1
    #time.sleep(1)
    python_is_fun()    


mydata.msg = "Justin rocks!" 

thread1 = threading.Thread(target=do_it, args=("thread1", "software is cool"))
thread1.start()

thread2 = threading.Thread(target=do_it2, args=("thread2", "programming is fun"))
thread2.start()

thread1.join()
thread2.join()

print(mydata.msg)
