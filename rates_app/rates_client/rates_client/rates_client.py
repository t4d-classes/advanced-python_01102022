""" rate client module """
from typing import Any
import sys
import socket

from rates_shared.utils import read_config

def main():

    try:

        config = read_config()

        with socket.socket(
                socket.AF_INET, socket.SOCK_STREAM) as socket_client:

            socket_client.connect(
                (config["server"]["host"], config["server"]["port"])
            )

            welcome_message = socket_client.recv(2048)

            print(welcome_message.decode("UTF-8"))

            while True:

                command = input("> ")

                if command == "exit":
                    break
                else:
                    socket_client.sendall(command.encode('UTF-8'))
                    print(socket_client.recv(2048).decode('UTF-8'))

    except ConnectionResetError:
        print("Server connection was closed.")

    except KeyboardInterrupt:
        pass

    sys.exit(0)
