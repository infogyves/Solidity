from brownie import accounts, config, network, AdvancedCollectible
from scripts.igx_library import get_account, OPENSEA_URL, get_contract, fund_with_link

igx_token_URI = "https://ipfs.io/ipfs/QmVnW5xwWW8rt76L6WNN2uizFqjpcB4t8NpeHJMbVyc2GW?filename=igx_nft.png"



def deploy_and_create():
    account = get_account()
    print(f"The acccount is: {account}")
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrf_coordinator"),
        get_contract("link_token"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],        
        {"from": account})
    fund_with_link(advanced_collectible.address)
    create_collectible_txn = advanced_collectible.createCollectible({"from": account})
    create_collectible_txn.wait(1)
    print(f"New token has been created!!!")
    print(f"Transaction Receipt: {create_collectible_txn}")
    return advanced_collectible, create_collectible_txn

def main():
    deploy_and_create()