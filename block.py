
import utility


class Block:

    def __init__(self, data, hash='', nonce=0, timestamp=0):
        self.data = data
        self.hash = hash
        self.nonce = nonce
        self.timestamp = timestamp

    def fill_block(self):
        """
        Fills in the block attributes - timestamp, nonce, and hash.

        Used for the genesis block
        """
        self.timestamp = utility.current_timestamp()
        self.nonce = utility.find_nonce(self.data, self.timestamp)
        self.hash = utility.create_hash(self.data, self.nonce, self.timestamp)

    @staticmethod
    def fill_from_json(data):
        """
        Fills in the block attributes from a JSON object.

        Parameters:
            data (dict): The JSON object to fill the block attributes from.

        Returns:
            Block
        """

        return Block(data['data'], data['hash'], data['nonce'], data['timestamp'])

    def to_json(self):
        return {
            'data': self.data,
            'hash': self.hash,
            'nonce': self.nonce,
            'timestamp': self.timestamp,
        }


