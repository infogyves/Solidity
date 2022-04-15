from unittest import mock
from brownie import FundMe, MockV3Aggregator, accounts, config, network
from scripts.FundMeLib import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def deploy_FundMe():
    # Get an account for deployment
    local_account = get_account()
    print("Local account is " + str(local_account))

    # Get price feeds
    # If we're on a persistent network such as Rinkeby, get their price feeds
    # Otherwise, use Mock price feeds for testing
    print(f"The active network is {network.show_active()}...")
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feeds"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
    fm_contract = FundMe.deploy(
        price_feed_address,
        {"from": local_account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )

    print(f"Contract deployed to {fm_contract.address}")
    return fm_contract


def main():
    deploy_FundMe()
