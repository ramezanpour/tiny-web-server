import socket

from request import Request
from response import Response
from config import Config
from datetime import datetime, timedelta

import os
import psutil
import threading


class Server:
    __root_path = Config['rootPath']

    def __init__(self):
        self.__socket = socket.socket()

    @staticmethod
    def print_memory_usage():
        process = psutil.Process(os.getpid())
        print(f'Memory used: {process.memory_info().rss / 1024 / 1024} MB')

    @staticmethod
    def process_request(connection, address, data):
        start_time = datetime.now().microsecond
        if data is None:
            print("No data received")
            connection.close()

        request = Request(data)
        print(
            f'Request received from {address[0]}. Resource: {request.url}')

        response = Response(Server.__root_path, request)

        connection.send(response.get_response())
        connection.close()
        end_time = datetime.now().microsecond
        print(
            f'Responded with {response.status_code} in {end_time - start_time}ms')

        Server.print_memory_usage()

    def start(self):
        try:
            port = Config['listenPort']
            self.__socket.bind(('', port))
            self.__socket.listen()
            workers = []
            while True:
                print(f'Listening on port {port}...')
                connection, address = self.__socket.accept()
                data = connection.recv(1024)
                t = threading.Thread(
                    target=self.process_request, args=(connection, address, data))
                workers.append(t)
                t.start()

                for index, worker in enumerate(workers):
                    if not worker.is_alive():
                        del workers[index]

        except KeyboardInterrupt:
            self.__socket.close()
            print('\nConnection Closed.\nGoodbye :)')
