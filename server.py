import socket

from request import Request
from response import Response
from config import Config
from datetime import datetime, timedelta

import os
import psutil


class Server:
    def __init__(self):
        self.__socket = socket.socket()
        self.__root_path = Config['rootPath']

    def start(self):
        try:
            port = Config['listenPort']
            self.__socket.bind(('', port))
            self.__socket.listen()
            while True:
                print(f'Listening on port {port}...')
                connetion, address = self.__socket.accept()
                data = connetion.recv(1024)
                start_time = datetime.now().microsecond
                if data is None:
                    print("No data received")
                    connetion.close()

                request = Request(data)
                print(
                    f'Request received from {address[0]}. Resource: {request.url}')

                response = Response(self.__root_path, request)

                connetion.send(response.get_response())
                connetion.close()
                end_time = datetime.now().microsecond
                print(
                    f'Responded with {response.status_code} in {end_time - start_time}ms')

                self.print_memory_usage()

        except KeyboardInterrupt:
            self.__socket.close()
            print('\nConnection Closed.\nGoodbye :)')

    def print_memory_usage(self):
        process = psutil.Process(os.getpid())
        print(f'Memory used: {process.memory_info().rss / 1024 / 1024} MB')
