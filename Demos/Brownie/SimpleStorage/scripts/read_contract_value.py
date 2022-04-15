from brownie import simpleStorage, accounts, config


def read_contract():
    # Pick the latest contract in the array/chain using "-1"
    latest_contract = simpleStorage[0]
    # Brownie already has address and abi in the "build" folder
    print(latest_contract.simpleRetrieve())


def main():
    read_contract()
