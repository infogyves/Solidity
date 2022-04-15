from brownie import simpleStorage, accounts


def test_deploySimpleStorage():
    # Any test automation follows the below process:
    # 1. Arrange (get everything in place)
    # Get an account/key to use with the smart contract
    local_account = accounts[0]

    # 2. Act (perform the action)
    # In this case, deploy the contract and get favorite number
    simpleStorageContract = simpleStorage.deploy({"from": local_account})
    favoriteNumber = simpleStorageContract.simpleRetrieve()
    expectedNumber = 25

    # 3. Assert (validate)
    assert favoriteNumber == expectedNumber


def test_updateSimpleStorage():
    # 1. Arrange (get everything in place)
    # Get an account/key to use with the smart contract AND deploy the smart contract
    local_account = accounts[0]
    simpleStorageContract = simpleStorage.deploy({"from": local_account})

    # 2. Act (perform the action)
    # In this case, store the new favorite number.
    favoriteNumber = 255
    simpleStorageContract.simpleStore(favoriteNumber, {"from": local_account})
    newFavoriteNumber = simpleStorageContract.simpleRetrieve()

    # 3. Assert (validate)
    assert favoriteNumber == newFavoriteNumber
