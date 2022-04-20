from brownie import accounts, config, network, SimpleCollectible
from scrips.igx_library import get_account

igx_token_URI = "https://ipfs.io/ipfs/QmcskTWYwkijJ5spcoGadxQaMxJCsYk9ZZUFLSb2mWsCYw?filename=igx.png"
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"


def main():
    account = get_account()
    simple_collectible = SimpleCollectible.deploy({"from": account})
    txn = simple_collectible.createCollectible(igx_token_URI, {"from": account})
    txn.wait(1)
    print(
        f"AWESOME! You can view your NFT at {OPENSEA_URL.format(simple_collectible.address, simple_collectible.tokenCounter()-1)}"
    )
