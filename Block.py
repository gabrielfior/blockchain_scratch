import json
from typing import Sequence

from Transaction import Transaction


class Block:

    @staticmethod
    def from_json_string(jsonString: str):
        dct = json.loads(jsonString)
        return Block(dct['index'], dct['timestamp'],
                     dct['transactions'], dct['proof'], dct['previous_hash'])

    def __init__(self, index: int, timestamp: int, transactions: Sequence[Transaction], proof: float, previous_hash : str):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.proof = proof
        self.previous_hash = previous_hash

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True)