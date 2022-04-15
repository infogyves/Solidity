from brownie import FundMe
from scripts.FundMeLib import get_account


def fund():
    fund_me = FundMe[-1]
    account = get_account()
    entrance_fee = fund_me.getUsdEntranceFee()
    print(entrance_fee)
    print(f"The current entry fee is {entrance_fee}")
    print("Funding...")
    fund_me.simpleFund({"from": account, "value": entrance_fee})


def withdraw():
    fund_me = FundMe[-1]
    account = get_account()
    print("Withdrawing...")
    fund_me.simpleWithdraw({"from": account})


def main():
    fund()
    withdraw()
