from brownie import (
    Lottery,
    config,
    network,
    accounts,
    MockV3Aggregator,
    Contract,
    VRFCoordinatorV2Mock,
    LinkToken,
    interface,
)
from web3 import Web3

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-infogyves"]
contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorV2Mock,
    "link_token": LinkToken,
}


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
    return accounts.add(config["wallets"]["IG_key"])


def get_contract(contract_name):
    """
    This function will grab the contract from brownie-config and return that contract.
    If no contract is available through config, it will deploy a MOCK contract and
    return that contract.
        Args:
            Contract Name (string) - e.g. "eth_usd_price_feed"
        Returns:
            brownie.network.contract.ProjectContract (the most recently deployed version
            of this contract)
    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


DECIMALS = 8
STARTING_PRICE = 200000000000


def fund_with_link(
    _contract_address, _account=None, _link_token=None, _amount=5000000000000000000
):
    account = _account if _account else get_account()
    # 1. One way is to create a link_token object using get_contract
    link_token = _link_token if _link_token else get_contract("link_token")
    # 2. Another way is using an interface... i.e. LinkTokenInterface.sol
    # link_token_contract = interface.LinkTokenInterface(_link_token.address)
    txn = link_token.transfer(_contract_address, _amount, {"from": account})
    txn.wait(1)
    print(f"LINK Tokens transferred. Contract funded!")
    return txn


def deploy_mocks(decimals=DECIMALS, initial_value=STARTING_PRICE):
    print(f"Deploying Mocks...")
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    GAS_PRICE_LINK = config["networks"][network.show_active()]["gas_price_link"]
    BASE_FEE = config["networks"][network.show_active()]["fee"]
    # BASE_FEE = 250000000000000000
    # print(f"BASE FEE = " + BASE_FEE)
    # print(f"GAS PRICE LINK = " + GAS_PRICE_LINK)
    VRFCoordinatorV2Mock.deploy(BASE_FEE, GAS_PRICE_LINK, {"from": account})
    print(f"Mocks deployed!")
