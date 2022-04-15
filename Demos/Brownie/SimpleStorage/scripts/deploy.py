from brownie import accounts, config, simpleStorage, network
import os


def deploy_simple_storage():
    # 3 Ways to get public keys or accounts:
    # Method 1: use one of the 10 fake local accounts
    print("Fetching local accounts/keys...")
    # local_account = accounts[3]
    local_account = get_account()
    print("Assigning 4th key in the list...")
    print("Using local key " + str(local_account))
    print("Deploying Contract...")
    simpleStorageContract = simpleStorage.deploy({"from": local_account})
    print("Contract " + str(simpleStorageContract) + " deployed!")
    # Calling contract retrieve() function
    favoriteNumber = simpleStorageContract.simpleRetrieve()
    print("Favorite Number is: " + str(favoriteNumber))
    print("Updating favorite number...")
    ssTransaction = simpleStorageContract.simpleStore(255, {"from": local_account})
    # Waiting to complete the block
    ssTransaction.wait(1)
    newFavoriteNumber = simpleStorageContract.simpleRetrieve()
    print("New favorite number is: " + str(newFavoriteNumber))

    # Method 2: Store private key in Brownie and use it (RECOMMENDED)
    # infogyves_account = accounts.load("infogyves-account")
    # print("Using encrypted Private Key from Brownie...")
    # print(infogyves_account)
    # Method 3: Store private keys in environment variables
    # print("Loading Private Key from .env file...")
    # env_account = accounts.add(os.getenv("INFOGYVES_KEY"))
    # print(env_account)
    # OR directly get it from the config file and no need for OS
    # config_account = accounts.add(config["wallets"]["IG_key"])
    # print("Loading Private Key from BROWNIE-CONFIG file...")
    # print(config_account)


def get_account():
    if network.show_active() == "development":
        return accounts[3]
    else:
        return accounts.add(config["wallets"]["IG_key"])


def main():
    print("Deploying Simple Storage...")
    deploy_simple_storage()
