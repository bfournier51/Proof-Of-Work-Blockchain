# Code to create your own Blockchain

"""
Data stored in JSON (Java Script Object Notation)
Fingerprinting done by using hash utilizing SHA256 hashing algorithm
Proof of Work Blockchain based
"""
# timestamp
from calendar import c
import datetime

# calculating the hash to add digital fingerprint to the blocks
import hashlib

# To store data in blockchain
import _json
from json import dumps

# Use Flask for creating the web app
# jsonify for displaying the blockchain
from flask, import Flask, jsonify


class Blockchain:
    """ This function creates the first block and sets hash to 0"""
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0')

    """ This function adds further blocks into the chain"""
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1, 'timestamp': str(datetime.datetime.now()), 'proof': proof, 'previous_hash': previous_hash}
        self.chain.append(block)
        return block

    """ This function displays the previous block"""
    def print_previous_block(self):
        return self.chain[-1]

    """ This function is for Proof of Work, used to mine new blocks"""
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operations = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode().hexdigest())
            if hash_operations[:5] == '00000':
                check_proof = True
            else:
                new_proof =+ 1
        
        return new_proof
    
    def hash(self,block):
        encoded_block = .json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1

        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False

            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operations = hashlib.sha256(str(proof**2 - previous_proof**2).encode().hexdigest())

            if hash_operations[:5] != '00000':
                return False
            previous_block = block
            block_index += 1

        return True

# Creating the Web App using Flask
app = Flask(__name__)

# Create the object of the class Blockchain
blockchain = Blockchain()

# For mining a new block
@app.route('/mine_block', methods = ['GET'])
def mine_block():
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)

    response = {'message': 'A block is MINED', 'index' : block['index'], 'timestamp': block['timestamp'], 'proof': block['proof'], 'previous_hash': block['previous_hash']}

    return jsonify(response), 200

# Display blockchain in json format
@app.route('/get_chain', methods = ['GET'])
def display_chain():
    response = {'chain': blockchain.chain, 'length': len(blockchain.chain)}

    return jsonify(response), 200

# Check validity of blockchain
@app.route('/valid', methods = ['GET'])
def valid():
    valid = blockchain.chain_valid(blockchain.chain)

    if valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200

# Run the flask server locally
app.run(host='127.0.0.1', port=5000)










