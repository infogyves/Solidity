from scripts.igx_library import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
from scripts.Advanced.deploy_and_create import deploy_and_create
from brownie import config, network
import pytest

def test_can_create_simple_collectible():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local nodes and local mainnet forks. Test aborted.")
    # Act
    random_number = 777
    advanced_collectible, create_collectible_txn = deploy_and_create()
    requestID = create_collectible_txn.events["requestedCollectible"]["requestID"]
    get_contract("vrf_coordinator").callBackWithRandomness(requestID,random_number,advanced_collectible.address, {"from": get_account})
    # Assert
    assert advanced_collectible.tokenCounter == 1

