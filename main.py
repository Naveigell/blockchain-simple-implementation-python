import sys

from flask import Flask, jsonify

from block import Block
from blockchain import Blockchain

blockchain = None
app = Flask(__name__)


@app.route('/blockchain', methods=['GET'])
def blockchain():
    return jsonify(blockchain.get_chain())


@app.route('/blockchain', methods=['POST'])
def store():
    block = Block({'vote': '4'})
    blockchain.add_waiting_block(block)

    return jsonify({
        'message': 'Block added to waiting list',
    }), 202


@app.route('/blockchain/mine', methods=['POST'])
def mine():
    blockchain.mine()

    return jsonify({
        'message': 'Block mined successfully',
    }), 201


@app.route('/blockchain/validate', methods=['GET'])
def validate():
    return jsonify({
        'message': 'Chain is valid' if blockchain.validate_chain() else 'Chain is not valid',
    })


@app.route('/blockchain/destroy', methods=['DELETE'])
def destroy():  # this method just for checking what if the block in blockchain is changed
    blockchain.chain[1].data = 9090

    return jsonify("Chain destroyed")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # please same port with env.py
    blockchain = Blockchain(int(sys.argv[1]))

    app.run(port=int(sys.argv[1]), debug=False)
