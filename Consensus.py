from typing import List

import requests

from Block import Block
from Blockchain import Blockchain
from ProofOfWork import ProofOfWork


class Consensus:

    @staticmethod
    def convert_chain_str_into_list_blocks(original_chain : List[str]):
        return [Block.from_json_string(i) for i in original_chain]

    @staticmethod
    def valid_chain(blockchain : Blockchain, chain : List[Block]):
        """
        Determine if a given blockchain is valid
        :return:
        """

        # parse list to list of blocks
        if not isinstance(chain[0], Block) and isinstance(chain[0], str):
            # convert list of strs to list of blocks
            chain = Consensus.convert_chain_str_into_list_blocks(chain)


        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n-----------\n")

            # Check that the hash of the block is correct
            if block.previous_hash != blockchain.hash(last_block):
                return False

            # Check that proof of work is correct
            if not ProofOfWork.valid_proof(last_block.proof, block.proof):
                return False

            last_block = block
            current_index += 1

        return True

    @staticmethod
    def resolve_conflicts(blockchain : Blockchain) -> [True, List[Block]]:
        """
        This is the consensus Algorithm, it resolves conflicts
        by determining the longest chain in the network.
        :param blockchain: Blockchain
        :return:
        """

        new_chain = None
        success = False

        # We are only looking for chains longer than ours
        max_length = len(blockchain.chain)

        # Grab and verify the chain from all other nodes in network
        for node in blockchain.nodes:
            response = requests.get(f'http://{node}/chain')

            if response.status_code != requests.codes.OK:
                print(f'Neighbour {node} could not be reached! Continuing...')
                continue

            print(response.json())
            length = response.json()['length']
            default_chain = Consensus.convert_chain_str_into_list_blocks(response.json()['chain'])
            print(f'default chain: {default_chain}')

            # Check that length is longer and the chain is valid
            if length > max_length and Consensus.valid_chain(blockchain, default_chain):
                max_length = length
                new_chain = default_chain

        # Return true if we discovered a new, valid chain longer than ours
        if new_chain:
            # blockchain.chain = new_chain
            success = True

        return [success, new_chain]



