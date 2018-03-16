import hashlib


class ProofOfWork:


    def proof_of_work(self, last_proof : str) -> int:
        """
        Simple Proof of Work algorithm:
            - Find number p which returns a valid proof after hashing with last_proof
        :param previous_hash: Hash of previous block
        :return:
        """

        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof : int, proof : int) -> bool:
        '''
        Validates the proof: Does hash(last_proof concat proof) contains 2 leading zeroes?
        :param last_proof: Previous proof
        :param proof: Current proof
        :return: bool whether proof is valid
        '''

        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:2] == "00"