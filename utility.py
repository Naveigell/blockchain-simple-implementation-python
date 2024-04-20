import hashlib
import json

import env

from datetime import datetime, timezone


def current_timestamp():
    """
    Returns the current timestamp in UTC.

    Returns:
        float: The current timestamp in UTC.
    """
    date_time = datetime.now(timezone.utc)
    utc_date_time = date_time.replace(tzinfo=timezone.utc)
    utc_date_time_in_timestamp = utc_date_time.timestamp()

    return utc_date_time_in_timestamp


def find_nonce(data, timestamp, previous_hash=''):
    """
    Finds and returns the nonce that satisfies the proof of work for the given data, timestamp, and previous_hash.

    Parameters:
    data (str): The data for which nonce needs to be found.
    timestamp (int): The timestamp of the data.
    previous_hash (str): The hash of the previous block (default is '').

    Returns:
    int: The nonce that satisfies the proof of work.
    """
    nonce = 0

    while not validate_proof_of_work(data, nonce, timestamp, previous_hash):
        nonce += 1

    return nonce


def validate_proof_of_work(data, nonce, timestamp, previous_hash=''):
    """
    Validates the proof of work by checking if the guess hash meets the target hash requirements.

    Parameters:
    data (str): The data to be included in the hash.
    nonce (int): The nonce value used for mining.
    timestamp (int): The timestamp of when the block was mined.
    previous_hash (str): The hash of the previous block.

    Returns:
    bool: True if the guess hash meets the target hash requirements, False otherwise.
    """
    # Create the guess hash using the provided data and parameters
    guess_hash = create_hash(data, nonce, timestamp, previous_hash)

    # Check if the beginning of the guess hash matches the target hash
    return guess_hash[:len(env.target)] == env.target


def create_hash(data, nonce, timestamp, previous_hash=''):
    """
    Create a hash based on the input data, nonce, timestamp, and previous hash.

    Args:
        data: The data to include in the hash.
        nonce: A random number used in hashing.
        timestamp: The timestamp of when the hash is created.
        previous_hash: The hash of the previous block in the blockchain.

    Returns:
        str: The hexadecimal representation of the generated hash.
    """
    content = json.dumps(str(data)) + str(nonce) + str(timestamp) + previous_hash

    return hashlib.sha256(content.encode('utf-8')).hexdigest()
