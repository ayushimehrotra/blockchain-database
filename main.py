import datetime
import hashlib
import json
import time
from tinyec import registry
from Crypto.Cipher import AES
import hashlib, secrets, binascii
import ast
import itertools
import pandas as pd
import numpy as np


class Block:
    def __init__(self, key, previous_hash, data: dict, primary_key):
        # hashing the primary key
        encoded_key = hashlib.sha256(str(hashlib.sha256(primary_key.encode()).hexdigest()).encode()).hexdigest()
        # Setting the block's right and left nodes
        self.left = None
        self.right = None
        # Block header with timestamp, previous hash, and key
        self.block_header = {'timestamp': str(datetime.datetime.now()),
                             'previous_hash': previous_hash,
                             'value': key
                             }
        # Block body with primary key and JSON
        self.block_body = {'primary_key': encoded_key,
                           'data': data
                           }


class BlockchainDatabase:

    def __init__(self):
        # initializing directory dictionary
        self.directory = {}
        # initializing blockchain database tree
        self.block_tree = Block(1, 0, (b'a', b'a', b'a'), "initial")
        self.number_of_blocks = 1

    def hash(self, block):
        # hashing a block
        return hashlib.sha256(str(hashlib.sha256(block).hexdigest()).encode()).hexdigest()

    def append(self, primary_key, data: dict, pubKey):
        # ECDH algorithm
        curve = registry.get_curve('secp192r1')
        encoded_key = hashlib.sha256(str(hashlib.sha256(primary_key.encode()).hexdigest()).encode()).hexdigest()
        root = self.block_tree
        directory = str((format(self.number_of_blocks + 1, "b"))) # converting number of blocks to binary directory
        temp_msg = str(data)
        msg = str.encode(temp_msg)
        ciphertextPrivKey = secrets.randbelow(curve.field.n)
        sharedECCKey = ciphertextPrivKey * pubKey
        sha = hashlib.sha256(int.to_bytes(sharedECCKey.x, 32, 'big'))
        sha.update(int.to_bytes(sharedECCKey.y, 32, 'big'))
        secretKey = sha.digest()
        aesCipher = AES.new(secretKey, AES.MODE_CTR)
        ciphertext = aesCipher.encrypt(msg)
        nonce = aesCipher.nonce
        ciphertextPubKey = ciphertextPrivKey * curve.g
        # end of ECDH algorithm
        for i in range(1, len(directory)):
            if i == len(directory) - 1: # if end of directory 
                if directory[i] == '1':
                    root.right = Block(self.number_of_blocks + 1, self.hash(root.block_body['data'][0]), (ciphertext, nonce, ciphertextPubKey), encoded_key)
                elif directory[i] == '0':
                    root.left = Block(self.number_of_blocks + 1, self.hash(root.block_body['data'][0]), (ciphertext, nonce, ciphertextPubKey), encoded_key)
            else:
                if directory[i] == '1':
                    root = root.right
                else:
                    root = root.left
        self.number_of_blocks += 1
        self.directory[encoded_key] = self.number_of_blocks # adding directory to new block

    def delete(self, primary_key):
        encoded_key = hashlib.sha256(str(hashlib.sha256(primary_key.encode()).hexdigest()).encode()).hexdigest()
        try:
            del self.directory[encoded_key] # deleting primary key from dictionary
        except KeyError:
            return "Key-Tuple pair previously deleted"

    def query(self, primary_key):
        encoded_key = hashlib.sha256(str(hashlib.sha256(primary_key.encode()).hexdigest()).encode()).hexdigest()
        root = self.block_tree
        if encoded_key not in self.directory:
            return "Data not in database"
        else:
            directory = str((format(self.directory[encoded_key], "b"))) # getting directory of block from dictionary
            for i in range(1, len(directory)):
                if directory[i] == '1':
                    root = root.right
                else:
                    root = root.left
            return root.block_body['data']

    def update(self, primary_key, data: dict, pubKey):
        # start of ECDH algorithm
        curve = registry.get_curve('secp192r1')
        encoded_key = hashlib.sha256(str(hashlib.sha256(primary_key.encode()).hexdigest()).encode()).hexdigest()
        try:
            del self.directory[encoded_key]
        except KeyError:
            return "Key-Tuple pair previously deleted"
        temp_msg = str(data)
        msg = str.encode(temp_msg)
        ciphertextPrivKey = secrets.randbelow(curve.field.n)
        sharedECCKey = ciphertextPrivKey * pubKey
        sha = hashlib.sha256(int.to_bytes(sharedECCKey.x, 32, 'big'))
        sha.update(int.to_bytes(sharedECCKey.y, 32, 'big'))
        secretKey = sha.digest()
        aesCipher = AES.new(secretKey, AES.MODE_CTR)
        ciphertext = aesCipher.encrypt(msg)
        nonce = aesCipher.nonce
        ciphertextPubKey = ciphertextPrivKey * curve.g
        root = self.block_tree
        directory = str((format(self.number_of_blocks + 1, "b"))) # converting number of blocks to binary directory
        for i in range(1, len(directory)):
            if i == len(directory) - 1:
                # appending new block 
                if directory[i] == '1':
                    root.right = Block(self.number_of_blocks + 1, self.hash(root.block_body['data'][0]), (ciphertext, nonce, ciphertextPubKey), encoded_key)
                elif directory[i] == '0':
                    root.left = Block(self.number_of_blocks + 1, self.hash(root.block_body['data'][0]), (ciphertext, nonce, ciphertextPubKey), encoded_key)
            else:
                if directory[i] == '1':
                    root = root.right
                else:
                    root = root.left
        self.number_of_blocks += 1
        self.directory[encoded_key] = self.number_of_blocks


curve = registry.get_curve('secp192r1')

privKey = secrets.randbelow(curve.field.n) # client needs to input right private key to access the data


def append_method(primary_key, data, privKey, blockchain):
    pubKey = privKey * curve.g
    blockchain.append(primary_key, data, pubKey)


def query_method(primary_key, privKey, blockchain):
    #start of ECDH algorithm
    (ciphertext, nonce, ciphertextPubKey) = blockchain.query(primary_key)
    sharedECCKey = privKey * ciphertextPubKey
    sha = hashlib.sha256(int.to_bytes(sharedECCKey.x, 32, 'big'))
    sha.update(int.to_bytes(sharedECCKey.y, 32, 'big'))
    secretKey = sha.digest()
    aesCipher = AES.new(secretKey, AES.MODE_CTR, nonce=nonce)
    plaintext = aesCipher.decrypt(ciphertext)
    dict = plaintext.decode()
    result = ast.literal_eval(dict)
    file = json.dumps(result)
    return file

def update_method(primary_key, data, privKey, blockchain):
    pubKey = privKey * curve.g
    blockchain.update(primary_key, data, pubKey)

def delete_method(primary_key, blockchain):
    blockchain.delete(primary_key)



def print_data_in_time_order(root):
    if root:
        print_data_in_time_order(root.left)
        print(root.block_header['value'])
        print_data_in_time_order(root.right)
