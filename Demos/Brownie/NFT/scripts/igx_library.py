from brownie import accounts, network, config

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
