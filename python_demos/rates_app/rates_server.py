""" rate server module """

from typing import Optional, Any
import multiprocessing as mp
from multiprocessing.sharedctypes import Synchronized
import sys
import socket
import threading
import re
import json
import requests
import mysql.connector
from contextlib import closing
import pathlib
import yaml

def read_config() -> Any:
    """ read config """

    with open(pathlib.Path("rates_app", "config", "rates_config.yaml")) as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.SafeLoader)


CLIENT_COMMAND_PARTS = [
    r"^(?P<command>[A-Z]*)",
    r"(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2})",
    r"(?P<symbol>[A-Z]{3})$"
]

client_command_regex = re.compile(" ".join(CLIENT_COMMAND_PARTS))

class ClientConnectionThread(threading.Thread):
    """ client connection thread """

    def __init__(
        self,
        conn: socket.socket,
        client_count: Synchronized,
        config: Any) -> None:

        threading.Thread.__init__(self)
        self.conn = conn
        self.client_count = client_count
        self.config = config

    def run(self) -> None:

        try:

            self.conn.sendall(b"Connected to the Rate Server")

            while True:
                client_command_bytes = self.conn.recv(2048)
                
                if not client_command_bytes:
                    break

                self.validate_client_command(client_command_bytes)

        except ConnectionAbortedError:
            ...

        finally:
            with self.client_count.get_lock():
                self.client_count.value -= 1


    def validate_client_command(self, client_command_bytes: bytes) -> None:
        """ validate the client command before processing """

        client_command_str = client_command_bytes.decode('UTF-8')

        client_command_match = client_command_regex.match(
            client_command_str
        )

        if not client_command_match:
            self.conn.sendall(b"Invalid Command Format")
        else:
            self.process_client_command(
                client_command_match.groupdict()
            )


    def process_client_command(self, client_command: dict[str, Any]) -> None:
        """ process client command """

        if client_command["command"] == "GET":

            with closing(mysql.connector.connect(
                host=self.config["database"]["host"],
                port=self.config["database"]["port"],
                user=self.config["database"]["username"],
                password=self.config["database"]["password"],
                database=self.config["database"]["name"],
            )) as db:

                sql = "select exchange_rate " \
                    "from rate " \
                    "where closing_date = %s and currency_symbol = %s"
            
                params = (client_command["date"], client_command["symbol"]) # create tuple with one element

                with closing(db.cursor(dictionary=True)) as cur:
                
                    cur.execute(sql, params)

                    rate = cur.fetchone()

                    if rate:
                        self.conn.sendall(str(rate["exchange_rate"])
                            .encode('UTF-8'))
                        return

                url = "".join([
                    "http://127.0.0.1:5000/api/",
                    client_command["date"],
                    "?base=USD&symbols=",
                    client_command["symbol"]
                ])

                response = requests.get(url)

                rate_data = json.loads(response.text)
                #rate_data = response.json()

                exchange_rate = rate_data["rates"][client_command["symbol"]]

                with closing(db.cursor()) as cur:

                    sql = "insert into rate (closing_date, currency_symbol, " \
                          "exchange_rate) values (%s, %s, %s)"

                    insert_params = (
                        client_command["date"],
                        client_command["symbol"],
                        exchange_rate)
                
                    cur.execute(sql, insert_params)

                    db.commit()

                    self.conn.sendall(
                        str(exchange_rate)
                        .encode('UTF-8'))

        else:
            self.conn.sendall(b"Invalid Command Name")


def rate_server(
  host: str, port: int,
  client_count: Synchronized, config: Any) -> None:
    """rate server"""

    with socket.socket(
        socket.AF_INET, socket.SOCK_STREAM) as socket_server:
        
        socket_server.bind( (host, port) )
        socket_server.listen()

        while True:

            conn, _ = socket_server.accept()

            with client_count.get_lock():
                client_count.value += 1

            client_con_thread = ClientConnectionThread(conn, client_count, config)
            client_con_thread.start()




def command_start_server(
    server_process: Optional[mp.Process],
    host: str, port: int, client_count: Synchronized,
    config: Any) -> mp.Process:
    """ command start server """

    if server_process and server_process.is_alive():
        print("server is already running")
    else:
        server_process = mp.Process(
            target=rate_server, args=(host, port, client_count, config))
        server_process.start()
        print("server started")

    return server_process


def command_stop_server(
    server_process: Optional[mp.Process]) -> Optional[mp.Process]:
    """ command stop server """

    if not server_process or not server_process.is_alive():
        print("server is not running")
    else:
        server_process.terminate()
        print("server stopped")

    server_process = None

    return server_process

def command_server_status(server_process: Optional[mp.Process]) -> None:
    """ output the status of the server """

    # typeguard
    if server_process and server_process.is_alive():
        print("server is running")
    else:
        print("server is stopped")


def command_count(client_count: Synchronized) -> None:
    """ command output connected client count """

    print(client_count.value)

def command_clear(config) -> None:

    with closing(mysql.connector.connect(
      host=config["database"]["host"],
      port=config["database"]["port"],
      user=config["database"]["username"],
      password=config["database"]["password"],
      database=config["database"]["name"],
    )) as db:

        with closing(db.cursor()) as cur:

            cur.execute("delete from rate")

            db.commit()


def command_exit(server_process: Optional[mp.Process]) -> None:
    """ exit the rates server app """

    if server_process and server_process.is_alive():
        server_process.terminate()


def main() -> None:
    """Main Function"""

    try:
        config = read_config()
        client_count: Synchronized = mp.Value('i', 0)
        server_process: Optional[mp.Process] = None
        
        host = config["server"]["host"]
        port = config["server"]["port"]

        while True:

            command = input("> ")

            if command == "start":
                server_process = command_start_server(
                    server_process, host, port, client_count, config)
            elif command == "stop":
                server_process = command_stop_server(server_process)
            elif command == "status":
                command_server_status(server_process)
            elif command == "count":
                command_count(client_count)
            elif command == "clear":
                command_clear(config)
            elif command == "exit":
                command_exit(server_process)
                break

    except KeyboardInterrupt:
        command_exit(server_process)

    sys.exit(0)


if __name__ == '__main__':
    main()