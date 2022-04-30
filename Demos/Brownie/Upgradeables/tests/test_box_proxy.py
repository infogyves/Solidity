from brownie import Box, ProxyAdmin, TransparentUpgradeableProxy, Contract
from scripts.box_lib import get_account, encode_function_data


def test_proxy_delegates_calls():
	# 1. Arrange:
    account = get_account()
    box = Box.deploy({"from": account})
    print(f"box.retrieve: {box.retrieve()}")
    proxy_admin = ProxyAdmin.deploy({"from": account})
    # 2. Act:
    box_encoded_initializer_function = encode_function_data()
    transparent_proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    proxy_box = Contract.from_abi("Box", transparent_proxy.address, Box.abi)
    # 3. Assert
    print(f"proxy_box.retrieve: {proxy_box.retrieve()}")
    assert proxy_box.retrieve() == 0
    proxy_box.store(255, {"from": account})
    assert proxy_box.retrieve() == 255


