from server import Server
from config import Config


import os

root_path = Config.get('rootPath', '')


if len(root_path) == '':
    print('Root path is required')
    exit(1)

root_path = os.path.realpath(root_path)
print(root_path)

if not os.path.isdir(root_path):
    print('Root path must be a directory')
    exit(2)


s = Server()
s.start()
