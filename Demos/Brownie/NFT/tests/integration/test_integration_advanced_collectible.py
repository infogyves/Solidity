from scripts.igx_library import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
from scripts.Advanced.deploy_and_create import deploy_and_create
from brownie import config, network
import pytest, time

def test_integration_can_create_advanced_collectible():
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Not for local testing. Use test on testnet. Test aborted.")
    # Act
    # Only for Unit Test
    # random_number = 777
    advanced_collectible, create_collectible_txn = deploy_and_create()
    time.sleep(60)
    # Only for Unit Test
    # get_contract("vrf_coordinator").callBackWithRandomness(requestID,random_number,advanced_collectible.address, {"from": get_account()})
    # Assert
    assert advanced_collectible.tokenCounter() == 1


