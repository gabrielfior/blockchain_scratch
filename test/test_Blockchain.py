import pytest

from Block import Block
from Blockchain import Blockchain

@pytest.fixture
def blockchain():
    return Blockchain()

def test_add_new_block(blockchain):
    initial_chain_size = len(blockchain.chain)
    added_block = blockchain.new_block(proof=2)

    assert initial_chain_size + 1 == len(blockchain.chain)
    assert isinstance(added_block, Block)


def test_last_block(blockchain):
    added_block = blockchain.new_block(proof=2)
    assert blockchain.last_block == added_block