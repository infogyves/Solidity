# Mints WETH by depositing ETH
from scripts.Igx_Aave_Library import get_account, get_contract
from brownie import interface, config, network


def main():
    get_weth()


def get_weth():
    # get the external account
    account = get_account()
    # get the WETH token from config
    weth = interface.IgxWethInterface(
        config["networks"][network.show_active()]["weth_key"]
    )
    print(f"Account {account}")
    print(f"WETH {weth}")
    txn = weth.deposit(
        {
            "from": account,
            "gas_limit": 350000,
            "allow_revert": True,
            "value": 1000000000000000000,
        }
    )
    print(f"Deposited 0.1 WETH")
    return txn
