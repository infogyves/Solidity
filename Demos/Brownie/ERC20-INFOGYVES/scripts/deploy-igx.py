from brownie import IGXToken
from web3 import Web3
from scripts.igx_library import get_account

initial_supply = Web3.toWei(1000, "ether")


def main():
    account = get_account()
    igx_token = IGXToken.deploy(initial_supply, {"from": account})
    print(igx_token.name())
