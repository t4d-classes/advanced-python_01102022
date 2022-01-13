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
from decimal import Decimal
from datetime import date, datetime

def read_config() -> Any:
    """ read config """

    with open(pathlib.Path("rates_app", "config", "rates_config.yaml")) as yaml_file:
        return yaml.load(yaml_file, Loader=yaml.SafeLoader)


def get_rate_from_api(closing_date: str, currency_symbol: str,
                      currency_rates: list[tuple[date, str, Decimal]]) -> None:
    """ get rate from api """

    url = "".join([
        "http://127.0.0.1:5000/api/",
        closing_date,
        "?base=USD&symbols=",
        currency_symbol,
    ])

    rate_data = requests.get(url).json()

    currency_rates.append(
        (datetime.strptime(closing_date, "%Y-%m-%d"),
         currency_symbol,
         Decimal(str(rate_data["rates"][currency_symbol]))))


CLIENT_COMMAND_PARTS = [
    r"^(?P<command>[A-Z]*) ",
    r"(?P<date>[0-9]{4}-[0-9]{2}-[0-9]{2}) ",
    r"(?P<symbol>[A-Z,:;|]*)$"
]

client_command_regex = re.compile("".join(CLIENT_COMMAND_PARTS))

currency_symbols_regex = re.compile(r"[,:;|]")


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

                currency_symbols = currency_symbols_regex.split(
                    client_command["symbol"])

                params = [client_command["date"]]
                params.extend(currency_symbols)

                placeholders = ",".join(["%s"] * len(currency_symbols))
                
                sql = "select currency_symbol, exchange_rate " \
                    "from rate " \
                    f"where closing_date = %s and currency_symbol in ({placeholders})"

                cached_currency_symbols: set[str] = set()

                rate_responses = []

                with closing(db.cursor(dictionary=True)) as cur:

                    cur.execute(sql, params)

                    cached_rates = cur.fetchall()

                    for cached_rate in cached_rates:
                        cached_currency_symbols.add(cached_rate["currency_symbol"])
                        rate_responses.append(
                            f"{cached_rate['currency_symbol']}: {cached_rate['exchange_rate']}")

                
                currency_rate_threads: list[threading.Thread] = []
                currency_rates: list[tuple[date, str, Decimal]] = []

                for currency_symbol in currency_symbols:
                    if currency_symbol not in cached_currency_symbols:

                        currency_rate_thread = threading.Thread(
                            target=get_rate_from_api,
                            args=(client_command["date"],
                                  currency_symbol, currency_rates))

                        currency_rate_thread.start()
                        currency_rate_threads.append(currency_rate_thread)

                for currency_rate_thread in currency_rate_threads:
                    currency_rate_thread.join()

                if len(currency_rates) > 0:

                    with closing(db.cursor()) as cur:

                        sql = " ".join([
                            "insert into rate",
                            "(closing_date, currency_symbol, exchange_rate)",
                            "values",
                            "(%s, %s, %s)",
                        ])

                        cur.executemany(sql, currency_rates)

                        db.commit()

                    for currency in currency_rates:
                        rate_responses.append(
                            f"{currency[1]}: {currency[2]}")

                self.conn.sendall(
                    "\n".join(rate_responses).encode("UTF-8"))

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