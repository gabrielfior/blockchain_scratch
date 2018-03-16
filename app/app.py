# Instantiate our Node
from uuid import uuid4
import requests
from flask import Flask, jsonify, request

from Blockchain import Blockchain
from Transaction import Transaction

app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()

@app.route('/mine', methods = ['GET'])
def mine():
    # We run the PoW to get the next proof
    last_block = blockchain.last_block
    last_proof = last_block.proof
    proof = blockchain.Proof_of_Work.proof_of_work(last_proof)

    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        Transaction(sender="0", recipient=node_identifier, amount=1,)
    )

    # Forge the new block by adding it to the chain
    previous_hash = blockchain.hash(last_block)
    block = blockchain.new_block(proof, previous_hash)

    response = {
        'message': 'New Block forged',
        'index': block.index,
        'transactions': block.transactions,
        'proof': block.proof,
        'previous_hash': block.previous_hash,
    }

    return jsonify(response), requests.codes.OK

@app.route('/transactions/new', methods = ['POST'])
def new_transaction():
    values = request.get_json()

    # Check that required fields are in the Post request
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', requests.codes.BAD_REQUEST

    # Creates a new transaction
    # TODO - write test
    index = blockchain.new_transaction(Transaction(values['sender'], values['recipient'], values['amount']))

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), requests.codes.CREATED

@app.route('/chain', methods = ['GET'])
def full_chain():
    # TODO - write tests
    # TODO2 - check if response can be better than below
    #{
    #    "chain": [
    #        "{\"index\": 1, \"previous_hash\": 1, \"proof\": 100, \"timestamp\": 1521227561.018, \"transactions\": []}"
    #    ],
    #    "length": 1
    #}

    response = {
        'chain': [i.toJson() for i in blockchain.chain],
        'length': len(blockchain.chain)
    }
    return jsonify(response), requests.codes.OK

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)