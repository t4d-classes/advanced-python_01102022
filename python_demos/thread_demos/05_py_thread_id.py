""" py thread id """

import threading

def do_it() -> None:

    print("did it")
    print(threading.get_ident())
    print(threading.current_thread().name)


thread1 = threading.Thread(target=do_it, name="thread1")
thread1.start();

thread2 = threading.Thread(target=do_it, name="thread2")
thread2.start();

thread1.join();
thread2.join();

print(threading.get_ident())
print(threading.current_thread().name)