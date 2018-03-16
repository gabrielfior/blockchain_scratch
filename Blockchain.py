from typing import List

import ProofOfWork
import Transaction
import hashlib
import json
from time import time
import hashlib
import json
from time import time
import Transaction
from Block import Block


class Blockchain:
    def __init__(self):

        self.chain: List[Block] = []
        self.current_transactions = []
        self.proof_of_work = ProofOfWork()

        # Genesis block
        self.new_block(previous_hash = 1, proof = 100)

    def new_block(self, proof : int, previous_hash : str = None) -> Block:
        '''
        Created new block and adds it to chain.
        :param proof: Proof given by Proof-of-Work algorithm
        :param previous_hash: (Optional) Hash of previous block.
        :return: Block object
        '''
        block = Block(
            index=len(self.chain) + 1,
            timestamp = time(),
            transactions = self.current_transactions,
            proof = proof,
            previous_hash = previous_hash or self.hash(self.chain[-1].toJson())
                      )

        #Reset current list of transactions
        self.current_transactions = []
        self.chain.append(block)

        return block

    def new_transaction(self, transaction : Transaction):
        '''
        Adds a new transaction to the list of transactions.
        :return:
        '''

        self.current_transactions.append(transaction.__dict__)
        return self.last_block.index + 1

    @staticmethod
    def hash(block : Block) -> str:
        '''
        Creates a SHA-256 hash of a block.
        :param block: Block object
        :return: calculated hash of the ordered block (to avoid inconsistencies)
        '''
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    @property
    def last_block(self) -> Block:
        '''
        Returns last block on the chain.
        :return:
        '''
        return self.chain[-1]