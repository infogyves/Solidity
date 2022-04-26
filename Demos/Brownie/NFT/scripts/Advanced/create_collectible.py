from brownie import AdvancedCollectible, network, config
from scripts.igx_library import get_account, fund_with_link
from web3 import Web3

def main():
    create_collectible()

def create_collectible():
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(advanced_collectible.address, _amount=Web3.toWei(0.1, "ether"))
    create_collectible_txn = advanced_collectible.createCollectible({"from": account})
    create_collectible_txn.wait(1)
    print(f"Collectible created! Transaction details: {create_collectible_txn}")



