from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol") as file:
    simple_storage_file = file.read()

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connection to Sepolia Testnet
w3 = Web3(
    Web3.HTTPProvider("https://sepolia.infura.io/v3/1e8cc3644a9c48a393ad3ff8789b3125")
)
chain_id = 11155111
my_address = "0x694f2d159321969f5d86b52B6a3E333fD9dce48c"
private_key = os.getenv("PRIVATE_KEY")

# Create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# Build Transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)

# Sign Transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# Send Transaction
print("Deploying Contract...")
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed")

# Working with contracts
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Call and Transation on functions
print(simple_storage.functions.retrieve().call())
print("Updating Contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce + 1}
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_txn = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
store_tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_txn)
print("Updated!")
print(simple_storage.functions.retrieve().call())
