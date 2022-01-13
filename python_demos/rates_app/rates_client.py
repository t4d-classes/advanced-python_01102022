""" rate client module """
from typing import Any
import sys
import socket
import pathlib
import yaml

def read_config() -> Any:
    """ read config """

    with open(pathlib.Path("rates_app", "config", "rates_config.yaml")) as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.SafeLoader)

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