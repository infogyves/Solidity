from brownie import (
    Box,
    BoxV2,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    Contract,
    exceptions,
)
import pytest
from scripts.box_lib import get_account, encode_function_data, upgrade


def test_box_v2_upgrades():
    # 1. Arrange
    account = get_account()
    box = Box.deploy({"from": account})
    print(f"boxV2.retrieve(): {box.retrieve()}")
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encoded_initializer_function = encode_function_data()
    transparent_proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    boxV2 = BoxV2.deploy({"from": account})
    proxy_box = Contract.from_abi("BoxV2", transparent_proxy.address, BoxV2.abi)
    # This should throw an error as we have not yet called the upgrade function!
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from": account})
    upgrade(account, transparent_proxy, boxV2, _proxy_admin_contract=proxy_admin)
    # NOW proxy should be pointing to the new implementation
    assert proxy_box.retrieve() == 0
    proxy_box.increment({"from": account})
    assert proxy_box.retrieve() == 1
