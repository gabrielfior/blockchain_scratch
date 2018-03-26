# Instantiate our Node
import optparse
import os
import sys
from uuid import uuid4

import requests
from flask import Flask, jsonify, request

path_of_file = os.path.abspath(os.path.dirname(__file__))
print(f'path of file: {path_of_file}')
parent = os.path.abspath((os.path.dirname(path_of_file)))
print(f'parentt: {parent}')
sys.path.append(parent)

from Blockchain import Blockchain
from Consensus import Consensus
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

@app.route('/nodes/register', methods=['POST'])
def register_node():

    values = request.get_json()
    nodes = values.get('nodes')

    if nodes is None:
        return "Error: Please supply a valid list of nodes", requests.codes.BAD_REQUEST

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }

    return jsonify(response), requests.codes.CREATED

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    success, new_chain = Consensus.resolve_conflicts(blockchain)

    if success:
        blockchain.chain = new_chain

        response = {
            'message': 'Our chain was replaced',
            'new_chain': [i.toJson() for i in blockchain.chain]
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': [i.toJson() for i in blockchain.chain]
        }

    return jsonify(response)

def flaskrun(app : Flask, default_host="127.0.0.1",
                  default_port="5000"):
    """
    Takes a flask.Flask instance and runs it. Parses
    command-line flags to configure the app.
    """

    # Set up the command-line options
    parser = optparse.OptionParser()
    parser.add_option("-H", "--host",
                      help="Hostname of the Flask app " + \
                           "[default %s]" % default_host,
                      default=default_host)
    parser.add_option("-P", "--port",
                      help="Port for the Flask app " + \
                           "[default %s]" % default_port,
                      default=default_port)

    # Two options useful for debugging purposes, but
    # a bit dangerous so not exposed in the help message.
    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug",
                      help=optparse.SUPPRESS_HELP)
    parser.add_option("-p", "--profile",
                      action="store_true", dest="profile",
                      help=optparse.SUPPRESS_HELP)

    options, _ = parser.parse_args()

    # If the user selects the profiling option, then we need
    # to do a little extra setup
    if options.profile:
        from werkzeug.contrib.profiler import ProfilerMiddleware

        app.config['PROFILE'] = True
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app,
                       restrictions=[30])
        options.debug = True

    app.run(
        debug=options.debug,
        host=options.host,
        port=int(options.port)
    )

if __name__ == "__main__":
    flaskrun(app)

