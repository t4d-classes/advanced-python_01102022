""" py thread class """

import threading

class DoItThread(threading.Thread):

    def __init__(self, msg: str) -> None:
        threading.Thread.__init__(self)

        self.msg = msg

    
    def run(self) -> None:

        print(self.msg + " " + str(threading.get_ident()))
        self.whoami("run method")

    
    def whoami(self, location: str) -> None:
        """ whoami """
        print(self.msg + ", " + location + ", " + str(threading.get_ident()))



some_thread = DoItThread("a message of hope and peace")
some_thread.start()

some_thread.whoami("main script")

