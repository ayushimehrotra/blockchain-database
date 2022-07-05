import datetime
import hashlib
import json
import timeit
import sys


class Block:
    def __init__(self, key, previous_hash, data: dict, primary_key):
        # encoded_key = hashlib.sha256(str(hashlib.sha256(primary_key.encode()).hexdigest()).encode()).hexdigest()
        self.left = None
        self.right = None
        self.block_header = {'timestamp': str(datetime.datetime.now()),
                             'previous_hash': previous_hash,
                             'value': key
                             }
        self.block_body = {'primary_key': primary_key,
                           'data': json.dumps(data)
                           }


class BlockchainDatabase:

    def __init__(self):
        self.directory = {}
        self.block_tree = Block(1, 0, {"test": 0}, "initial")
        self.number_of_blocks = 1

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True)
        return hashlib.sha256(str(hashlib.sha256(encoded_block.encode()).hexdigest()).encode()).hexdigest()

    def print_data_in_time_order(self, root):
        if root:
            print_data_in_time_order(root.right)
            print(root.block_header['value'])
            print_data_in_time_order(root.left)

    def append(self, primary_key, data: dict):
        root = self.block_tree
        directory = str((format(self.number_of_blocks + 1, "b")))
        for i in range(1, len(directory)):
            if i == len(directory) - 1:
                if directory[i] == '1':
                    root.right = Block(self.number_of_blocks + 1, self.hash(root.block_body), data, primary_key)
                elif directory[i] == '0':
                    root.left = Block(self.number_of_blocks + 1, self.hash(root.block_body), data, primary_key)
            else:
                if directory[i] == '1':
                    root = root.right
                else:
                    root = root.left
        self.number_of_blocks += 1
        self.directory[primary_key] = self.number_of_blocks

    def delete(self, primary_key):
        try:
            del self.directory[primary_key]
        except KeyError:
            return "Key-Tuple pair previously deleted"

    def query(self, primary_key):
        root = self.block_tree
        if primary_key not in self.directory:
            return "Data not in database"
        else:
            directory = str((format(self.directory[primary_key], "b")))
            for i in range(1, len(directory)):
                if directory[i] == '1':
                    root = root.right
                else:
                    root = root.left
            return root.block_body['data']
