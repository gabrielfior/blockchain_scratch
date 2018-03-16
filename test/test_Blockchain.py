import pytest

from Block import Block
from Blockchain import Blockchain


class A_Helper:
    def __init__(self, fixture):
        print ("In class A_Helper")

    def some_method_in_a_helper(self):
        print ("foo")

class Test_class:
    @classmethod
    def setup_class(cls):
        print ("!!! In setup class !!!")
        cls.blockchain = Blockchain()

    def test_add_new_block(self):
        initial_chain_size = len(self.blockchain.chain)
        added_block = self.blockchain.new_block(proof=2)

        assert initial_chain_size + 1 == len(self.blockchain.chain)
        assert isinstance(added_block, Block)


    def test_last_block(self):
        added_block = self.blockchain.new_block(proof=2)
        assert self.blockchain.last_block == added_block