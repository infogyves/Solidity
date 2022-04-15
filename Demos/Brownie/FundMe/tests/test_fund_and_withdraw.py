import pytest
from scripts.FundMeLib import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_FundMe
from brownie import network, accounts, exceptions


def test_can_fund_and_withdraw():
    # 1. Arrange
    account = get_account()
    fund_me = deploy_FundMe()
    entrance_fee = fund_me.getUsdEntranceFee() + 100
    # 2. Act
    txn_f = fund_me.simpleFund({"from": account, "value": entrance_fee})
    txn_f.wait(1)
    # 3. Assert
    assert fund_me.simpleAddresstoFundAmount(account.address) == entrance_fee
    # Repeat #2. for Withdraw
    txn_w = fund_me.simpleWithdraw({"from": account})
    txn_w.wait(1)
    # Repeat #3. for Withdraw
    assert fund_me.simpleAddresstoFundAmount(account.address) == 0


def test_onlyOwner_can_withdraw():
    # 1. Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Test terminated! Only for test in local environments.")
    # 2. Act
    fund_me = deploy_FundMe()
    entrance_fee = fund_me.getUsdEntranceFee()
    bad_actor = accounts.add()
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.simpleWithdraw({"from": bad_actor})
