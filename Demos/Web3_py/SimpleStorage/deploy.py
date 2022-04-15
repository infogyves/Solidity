import os
from solcx import compile_standard
import json
from web3 import Web3
import os
from dotenv import load_dotenv

load_dotenv()

with open("./SimpleStorage.sol", "r") as ssFile:
    simple_storage_file = ssFile.read()

# Having read the solidity code for our contract, compile it.
compiled_contract = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourcemap"]}
            }
        },
    },
    # solc_version="0.6.0",
)

# Print this code to stdout
# print(compiled_contract)

# Save ABI to json file
with open("SimpleStorage.json", "w") as ssJsonFile:
    json.dump(compiled_contract, ssJsonFile)

# To deploy the contract, we need "Bytecode" and "abi"...

# Get bytecode
ssBytecode = compiled_contract["contracts"]["SimpleStorage.sol"]["simpleStorage"][
    "evm"
]["bytecode"]["object"]

# Get abi
ssAbi = compiled_contract["contracts"]["SimpleStorage.sol"]["simpleStorage"]["abi"]

# Connecting to Ganache
gW3Server = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/c03be5f6d0da48c7b5d1f85849aa5bf4")
)
gChainID = 4
gPublicKey = "0x370E34336f210179b511e3C683DE017cE53bdb89"
# gPrivateKey = "0x440b84c696cf1f5a62af171bdc200e1b1a968e1dc802a8109f1d7286bc67dd6b"
gPrivateKey = os.getenv("PRIVATE_KEY")

# Create the contract in Python
SimpleStorage = gW3Server.eth.contract(abi=ssAbi, bytecode=ssBytecode)
# print(SimpleStorage)

# Working with TRANSACTIONS
# 1. Build the Transaction
# 2. Sign the Transaction
# 3. Send the transaction

# Build the transaction
# Get latest transaction count to use as NONCE
nonce = gW3Server.eth.getTransactionCount(gPublicKey)
print(nonce)

ssTransaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": gW3Server.eth.gas_price,
        "chainId": gChainID,
        "from": gPublicKey,
        "nonce": nonce,
    }
)
# print(ssTransaction)

print(gPrivateKey)

# Sign the transaction
signed_ssTransaction = gW3Server.eth.account.sign_transaction(
    ssTransaction, private_key=gPrivateKey
)
# print(signed_ssTransaction)

# Send the Transaction
hash_ssTransaction = gW3Server.eth.send_raw_transaction(
    signed_ssTransaction.rawTransaction
)

transactionReceipt = gW3Server.eth.wait_for_transaction_receipt(hash_ssTransaction)

# Working with SMART CONTRACTS
# To create a smart contract, you need a) the ABI, and b) the public key
ssContract = gW3Server.eth.contract(
    address=transactionReceipt.contractAddress, abi=ssAbi
)

# CALL - is similar to the BLUE button in REMIX.
# It return a value, but does not cause a state change
print(ssContract)
print(ssContract.functions.simpleRetrieve().call())

# TRANSACT - is similar to the ORANGE button in REMIX
# It causes a state change and need to build, sign, send the transaction
# Build:
ssStoreTxn = ssContract.functions.simpleStore(255).buildTransaction(
    {
        "gasPrice": gW3Server.eth.gas_price,
        "chainId": gChainID,
        "from": gPublicKey,
        "nonce": nonce + 1,
    }
)
print(ssStoreTxn)

# Sign:
signed_ssStoreTxn = gW3Server.eth.account.sign_transaction(
    ssStoreTxn, private_key=gPrivateKey
)

# Send:
hash_signed_ssStoreTxn = gW3Server.eth.send_raw_transaction(
    signed_ssStoreTxn.rawTransaction
)
rcpt_signed_ssStoreTxn = gW3Server.eth.wait_for_transaction_receipt(
    hash_signed_ssStoreTxn
)
print(ssContract.functions.simpleRetrieve().call())
