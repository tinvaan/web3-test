import sys

from web3 import Web3
from web3.exceptions import InvalidAddress, CannotHandleRequest


def connect_provider(url):
    w3 = Web3(Web3.HTTPProvider(url))
    if w3.isConnected():
        return w3
    else:
        raise CannotHandleRequest


def get_contract(w3, address):
    try:
        contract = w3.eth.contract(address)
    except InvalidAddress:
        print("Invalid contract. Please check the contract address again.")
    return contract


def get_block_hash(contract):
    block_number = contract.web3.eth.blockNumber
    block = contract.web3.eth.getBlock(block_number)
    return block.hash


if __name__ == "__main__":
    if "--host" in sys.argv and len(sys.argv) == 4:
        address = sys.argv[1]
        domain = sys.argv[3]
    elif len(sys.argv) == 3:
        address = sys.argv[1]
        domain = sys.argv[2]
    else:
        print("Invalid arguments provided", sys.stderr)
        print("Usage : script <contract address> [--host] <web3 host domain>")

    try:
        w3 = connect_provider(domain)
        contract = get_contract(w3, address)
        block_hash = get_block_hash(contract)

        print("Contract block hash : ", block_hash)
    except CannotHandleRequest:
        print("Failed to connect to web provider at ", domain, sys.stderr)
    except Exception as e:
        print(e)
