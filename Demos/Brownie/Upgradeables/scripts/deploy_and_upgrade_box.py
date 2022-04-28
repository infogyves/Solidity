from brownie import (
    network,
    Box,
    BoxV2,
    ProxyAdmin,
    Contract,
    TransparentUpgradeableProxy,
)
from scripts.box_lib import get_account, encode_function_data


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
    print("You can now upgrade to Box V2!")
    # Associating the proxy to the box:
    proxy_box = Contract.from_abi("Box", transparent_proxy.address, Box.abi)
    print(f"proxy_box.store: 255")
    txn = proxy_box.store(255, {"from": account})
    txn.wait(1)
    print(f"proxy_box.retrieve: {proxy_box.retrieve()}")
    proxy_box.increment()

    # Now, deploy BoxV2 (the upgraded Box)


def main():
    print(f"Starting proxy demo on {network.show_active()} network!")
    deploy_and_upgrade_box()
