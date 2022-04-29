from brownie import network, config, accounts
import eth_utils

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-infogyves"]


def get_account(index=None, id=None):
    # If there is an index passed, use the index
    # Else if there an account available (e.g. infogyes), use that
    # If none is available, default to config files
    print(f"The active account is {network.show_active()}")
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        print(f"Fetching {network.show_active()} Account...")
        return accounts[3]
    # If none of the above:
    print("Fetching Testnet account...")
    return accounts.add(config["wallets"]["priv_key"])


# Encoding function that takes initializer and any number of arguments as parameters
# In the Box.sol example, initalizer is them implementation contract i.e. box,
# and arguments could be 1, 2, 3, 4 etc.
def encode_function_data(initializer=None, *args):
    if len(args) == 0 or not initializer:
        return eth_utils.to_bytes(hexstr="0x")
    return initializer.encode_input(*args)


# Upgrade wrapper function that swaps out old implementation for new implementation
# by taking the new implementation, proxy, an account, proxy_admin as parameters
def upgrade(
    _account,
    _proxy,
    _new_implementation_address,
    _proxy_admin_contract=None,
    _initializer=None,
    *args,
):
    txn = None
    if _proxy_admin_contract:
        if _initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            txn = _proxy_admin_contract.upgradeAndCall(
                _proxy.address,
                _new_implementation_address,
                encoded_function_call,
                {"from": _account},
            )
        else:
            txn = _proxy_admin_contract.upgrade(
                _proxy.address,
                _new_implementation_address,
                {"from": _account},
            )
    else:
        if _initializer:
            encoded_function_call = encode_function_data(initializer, *args)
            txn = _proxy.upgradeToAndCall(
                _new_implementation_address,
                encoded_function_call,
                {"from": _account},
            )
        else:
            txn = _proxy_admin_contract.upgradeTo(
                _new_implementation_address,
                {"from": _account},
            )
    return txn
