from typing import List

import env
import utility
import requests
from block import Block


class Blockchain:

    def __init__(self, port: int):
        """
        Initialize the Blockchain with the given port.

        Parameters:
            port (int): The port number to initialize the Blockchain.

        Returns:
            None
        """
        # Set the port for the Blockchain
        self.port = port

        # Initialize the chain and waiting_blocks lists
        self.chain: List[Block] = []
        self.waiting_blocks: List[Block] = []

        # Create a new block with a vote and fill it
        block = Block([{'vote': '2'}])
        block.fill_block()

        # Add the newly created block to the chain
        self.add_block(block)

    def mine(self):
        """
        Mines a new block by finding the correct nonce value and adding the block to the blockchain.

        Returns:
            bool: True if a new block is successfully mined and added, False otherwise.
        """

        # Check if there are any waiting blocks to mine
        if len(self.waiting_blocks) == 0:
            return False

        # Get the latest block in the blockchain
        latest_block = self.last_block()

        # Get the data of waiting blocks
        waiting_blocks = self.get_waiting_blocks_data()

        # Generate timestamp for the block
        timestamp = utility.current_timestamp()

        # Find the correct nonce value for the block
        nonce = utility.find_nonce(waiting_blocks, timestamp, latest_block.hash)

        # Create the hash for the new block
        hash = utility.create_hash(waiting_blocks, nonce, timestamp, latest_block.hash)

        # Add the newly mined block to the blockchain
        self.add_block(Block(waiting_blocks, hash, nonce, timestamp))

        # Clear the waiting blocks list
        self.waiting_blocks = []

        return True

    def get_waiting_blocks_data(self):
        """
        Get the data of waiting blocks.

        Returns:
            Union[List[Dict], Dict]: The data of the waiting blocks.
        """
        if len(self.waiting_blocks) == 1:
            # if the length of the waiting blocks is 1, we only get the data, the data will be converted again
            # in create_hash() function
            return self.waiting_blocks[0].data

        return [block.data for block in self.waiting_blocks]

    def validate_chain(self):
        """
        Validates the integrity of the blockchain by checking if each block's hash is correctly calculated based on its data and previous block's hash.

        Returns:
            bool: True if the chain is valid, False otherwise.
        """

        for i in range(1, len(self.chain)):
            # check if the current hash and the current data with previous hash is correct
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if not current_block.hash == utility.create_hash(current_block.data, current_block.nonce,
                                                             current_block.timestamp, previous_block.hash):
                return False

        return True

    def add_waiting_block(self, block):
        """
        Adds a waiting block to the list of waiting blocks.

        Parameters:
            block (Block): The block to be added to the waiting_blocks list.

        Returns:
            None
        """
        self.waiting_blocks.append(block)

    def add_block(self, block: Block):
        """
        Adds a block to the blockchain chain.

        Parameters:
            block (Block): The block to be added to the chain.

        Returns:
            None
        """
        self.chain.append(block)

    def get_chain(self):
        """
        Get the chain of blocks in the blockchain.

        Returns:
            List[Dict]: The list of dictionaries representing each block in the chain.
        """
        return [block.to_json() for block in self.chain]

    def consensus(self):
        """
        Synchronizes the blockchain with the longest chain in the network.

        Returns:
            None
        """
        # filter nodes that are not the current node
        nodes = filter(lambda port: port != self.port, env.nodes)

        max_length = len(self.chain)

        for node in nodes:
            try:
                # try to get the blockchain from the other node
                response = requests.get(f'http://localhost:{node}/blockchain')
                chain = response.json()

                # check if the response is successful and the chain is longer than the current chain
                if response.status_code == 200:
                    length = len(chain)

                    # if the chain is longer and valid, update the current chain
                    if length >= max_length and self.validate_chain():
                        max_length = length
                        # update the chain with looping the chain and fill the block
                        self.chain = [Block.fill_from_json(block) for block in chain]

            except requests.exceptions.ConnectionError:
                # sometimes the connection is refused, so we just continue to the next node
                continue

    def last_block(self):
        """
        Retrieve the last block from the chain.

        Returns:
        Block: The last block in the chain.
        """
        return self.chain[-1]
