from scripts.lottery_library import get_account, get_contract, fund_with_link
from brownie import Lottery, network, config
import time

# account = get_account(id="infogyves-account")
# DEPLOY Lottery
# This happens only ONCE
def deploy_lottery():
    # account = get_account(id="infogyves-account")
    account = get_account()
    Lottery.deploy(
        # address _pPriceFeedAddress,
        # address _vrfCoordinator,
        # address _link,
        # uint256 _fee,
        # bytes32 _keyhash
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Lottery deployed successfully!")


# START Lottery
def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    starting_txn = lottery.startLottery({"from": account})
    starting_txn.wait(1)
    print("The lottery has started!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    entrance_fee = lottery.getEntranceFees() + 100000000
    print(f"Entrance Fees: {entrance_fee}")
    txn = lottery.enter({"from": account, "value": entrance_fee})
    txn.wait(1)
    print(f"Success! You've entered the Lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # Decide a winner (requestRandomness will take care of this!)
    # Fund the contract
    txn = fund_with_link(lottery.address)
    txn.wait(1)
    # Mark lottery as CLOSED
    ending_txn = lottery.endLottery({"from": account})
    ending_txn.wait(1)
    # The randomness function needs to do a callback; hence:
    time.wait(60)
    print(f"{lottery.recentWinner()} is the new Winner!")


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()
