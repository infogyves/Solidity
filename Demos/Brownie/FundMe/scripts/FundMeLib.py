from brownie import config, network, accounts, MockV3Aggregator
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-infogyves"]
DECIMALS = 8
STARTING_PRICE = 200000000000


def get_account():
    print(f"The active account is {network.show_active()}")
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        print(f"Fetching {network.show_active()} Account...")
        return accounts[3]
    else:
        print("Fetching Testnet account...")
        return accounts.add(config["wallets"]["IG_key"])


def deploy_mocks():
    print(f"Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
    print(f"Mocks deployed!")
