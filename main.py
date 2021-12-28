import datetime
import hashlib
import json
import timeit


class BlockchainDatabase:

    def __init__(self):
        self.append_chain = []
        self.delete_chain = []
        self.appends(previous_hash='0', data={'test': '0'}, sortkey='initial')
        self.delete(previous_hash='0', sortkey='initial')

    def appends(self, previous_hash, data: dict, sortkey):
        block = {'Block Header':
                     dict(index=len(self.append_chain) + 1, timestamp=str(datetime.datetime.now()),
                          previous_hash=previous_hash)
            ,
                 'Block Body':
                     {
                         'key': hashlib.sha256(sortkey.encode()).hexdigest(),
                         'data': data
                     }

                 }
        self.append_chain.append(block)
        return block

    def delete(self, previous_hash, sortkey):
        block = {'Block Header':
                     dict(index=len(self.delete_chain) + 1, timestamp=str(datetime.datetime.now()),
                          previous_hash=previous_hash)
            ,
                 'Block Body':
                     {
                         'key': hashlib.sha256(sortkey.encode()).hexdigest(),
                     }

                 }
        self.delete_chain.append(block)
        return block

    def print_previous_block_append(self):
        return self.append_chain[-1]

    def print_previous_block_delete(self):
        return self.delete_chain[-1]

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def query(self, append_chain, delete_chain, sortkey):
        block_index = 0
        temp_return = 0
        while block_index < len(append_chain):
            appblock = append_chain[block_index]
            if appblock['Block Body']['key'] == sortkey:
                temp_return = appblock['Block Body']['data']
            block_index += 1

        block_index = 0
        while block_index < len(delete_chain):
            delblock = delete_chain[block_index]
            if delblock['Block Body']['key'] == sortkey and temp_return != 0:
                return 'Data deleted'
            block_index += 1
        if temp_return == 0:
            return 'Data not found'
        else:
            return temp_return


blockchain = BlockchainDatabase()


def display_chain():
    response = {'chain': blockchain.delete_chain,
                'length': len(blockchain.delete_chain)}
    return response


def query_function(sortkey):
    start = timeit.default_timer()
    need = blockchain.query(blockchain.append_chain, blockchain.delete_chain, sortkey)
    end = timeit.default_timer()
    return need, end - start


def append_function(sortkey, data):
    previous_block_hash = blockchain.hash(blockchain.print_previous_block_append())
    blockchain.appends(previous_block_hash, data, sortkey)


def delete_function(sortkey):
    previous_block_hash = blockchain.hash(blockchain.print_previous_block_delete())
    blockchain.delete(previous_block_hash, sortkey)
    
    
