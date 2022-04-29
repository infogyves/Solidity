from brownie import (
    network,
    Box,
    BoxV2,
    ProxyAdmin,
    Contract,
    TransparentUpgradeableProxy,
)
from scripts.box_lib import get_account, encode_function_data, upgrade


def deploy_and_upgrade_box():
    account = get_account()
    print(f"Deploying Box to {network.show_active()} network...")
    # Deploy the Box contract
    box = Box.deploy({"from": account})
    print(f"box.retrieve: {box.retrieve()}")
    # Deploy a proxy contract
    proxy_admin = ProxyAdmin.deploy({"from": account})
    # Encode the initializer function!
    box_encoded_initializer_function = encode_function_data()

    transparent_proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    print(f"Proxy deployed to {transparent_proxy}")
    # Associating the proxy to the box:
    proxy_box = Contract.from_abi("Box", transparent_proxy.address, Box.abi)
    print(f"proxy_box.store: 255")
    txn = proxy_box.store(255, {"from": account})
    txn.wait(1)
    print(f"proxy_box.retrieve: {proxy_box.retrieve()}")
    print("You can now upgrade to BoxV2!")

    # Now, deploy BoxV2 (the upgraded Box)
    print("Deploying BoxV2!")
    box_v2 = BoxV2.deploy({"from": account})
    upgraded_txn = upgrade(
        account, transparent_proxy, box_v2.address, _proxy_admin_contract=proxy_admin
    )
    upgraded_txn.wait(1)
    print("Upgrading proxy to BoxV2!")
    proxy_box = Contract.from_abi("BoxV2", transparent_proxy.address, box_v2.abi)
    print("Proxy upgraded!!!")
    print(f"proxy_box.retrieve: {proxy_box.retrieve()}")
    print("Calling proxy_box.increment: ")
    inc_txn = proxy_box.increment({"from": account})
    inc_txn.wait(1)
    print(f"proxy_box.retrieve: {proxy_box.retrieve()}")


def main():
    print(f"Starting proxy demo on {network.show_active()} network!")
    deploy_and_upgrade_box()
