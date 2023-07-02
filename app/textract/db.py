"""
A file to handle all database interactions.
"""

from dataclasses import dataclass
import os
import atexit
from pathlib import Path

class DB:
    def __init__(self, path, cleanup_on_exit=False):
        self.path = Path(path).absolute()
        self.hash_map_ktv = {}
        self.hash_map_vtk = {}
        self.binary_keys = set()

        os.makedirs(self.path, exist_ok=True)
        
        if cleanup_on_exit:
            atexit.register(self.cleanup)

    def __getitem__(self, key):
        mode = 'rb' if key in self.binary_keys else 'r'
        with open(self.path / key, mode) as f:
            return f.read()

    def __setitem__(self, key, val):
        mode = 'wb' if key in self.binary_keys else 'w'
        with open(self.path / key, mode) as f:
            if mode == 'wb':
                f.write(val)
            else:
                f.write(str(val))

    def add(self, path_to_file):

        # get the filename and extension
        filename = path_to_file.split('/')[-1]
        extension = filename.split('.')[-1]

        # get the hash of the filename and store it in the bidirectional hash maps
        hash_id = hash(filename)
        hash_key = f"{hash_id}.{extension}"
        
        self.hash_map_ktv[hash_key] = filename
        self.hash_map_vtk[filename] = hash_key

        # if the file is not a text file, set it to binary
        if not extension in ['txt', 'json', 'csv']:
            self.set_binary(hash_key)
            mode = 'rb'
        else:
            mode = 'r'

        # read the file
        value = open(path_to_file, mode).read()

        # move the file to the database
        self[hash_key] = value

        # return the hash_key
        return hash_key

    def get(self, hash_key=None, filename=None):
        if hash_key:
            filename = self.hash_map_ktv[hash_key]
        elif filename:
            hash_key = self.hash_map_vtk[filename]
        else:
            raise ValueError('Either hash_id or filename must be provided.')

        return self[hash_key]

    def set_binary(self, key):
        self.binary_keys.add(key)
    
    def cleanup(self):
        for filename in os.listdir(self.path):
            os.remove(self.path / filename)


# dataclass for all dbs:
@dataclass
class DBs:
    memory: DB
    inputs: DB


if __name__ == '__main__':
    dbs = DBs(
        memory=DB('dbs/memory', cleanup_on_exit=True),
        inputs=DB('dbs/inputs', cleanup_on_exit=True),
    )
    dbs.memory.add('documents/tests/pdf_tests/test.pdf')
    print(dbs.memory.get(filename='test.pdf'))