from brownie import accounts, config, network, SimpleCollectible
from scripts.igx_library import get_account, OPENSEA_URL

igx_token_URI = "https://ipfs.io/ipfs/QmVnW5xwWW8rt76L6WNN2uizFqjpcB4t8NpeHJMbVyc2GW?filename=igx_nft.png"


def deploy_and_create():
    account = get_account()
    print(f"The acccount is: {account}")
    simple_collectible = SimpleCollectible.deploy({"from": account})
    txn = simple_collectible.createCollectible(igx_token_URI, {"from": account})
    txn.wait(1)
    print(
        f"AWESOME! You can view your NFT at {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter()-1)}"
    )
    return simple_collectible

def main():
    deploy_and_create()