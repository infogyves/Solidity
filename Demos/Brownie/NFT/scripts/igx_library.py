from brownie import accounts, network, config, Contract, AdvancedCollectible, VRFCoordinatorMock, LinkToken
from web3 import Web3
from pathlib import Path
import requests
import os

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-infogyves"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
LOGO_MAPPING = {0: "BLACK", 1: "WHITE", 2: "COLOUR"}


contract_to_mock = {
    "vrf_coordinator": VRFCoordinatorMock,
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
    return accounts.add(config["wallets"]["priv_key"])


def get_contract(contract_name):
    """
    This function grabs the name from brownie-config (e.g. "eth_usd_price_feed")
    and returns the contract associated with it.
    If no contract is available in config, it will deploy a MOCK contract and return
    that value.
    """
    contract_type = contract_to_mock[contract_name]
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    print(f"Deploying Mocks...")
    account = get_account()
    # MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    ####
    # Deploying Link Token
    print(f"Deploying Link Token...")
    link_token = LinkToken.deploy({"from": account})
    print(f"LINK TOKEN Deployed!!!")
    GAS_PRICE_LINK = config["networks"][network.show_active()]["gas_price_link"]
    BASE_FEE = config["networks"][network.show_active()]["fee"]
    # BASE_FEE = 250000000000000000
    # print(f"BASE FEE = " + BASE_FEE)
    # print(f"GAS PRICE LINK = " + GAS_PRICE_LINK)
    print(f"Deploying VRF Coordinator...")
    vrf_coordinator =VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print(f"VRF COORDINATOR Deployed!!!")
    print(f"ALL Mocks deployed!")

def fund_with_link(
    _contract_address, _account=None, _link_token=None, _amount=Web3.toWei(1, "ether")
):
    account = _account if _account else get_account()
    # 1. One way is to create a link_token object using get_contract
    link_token = _link_token if _link_token else get_contract("link_token")
    # 2. Another way is using an interface... i.e. LinkTokenInterface.sol
    # link_token_contract = interface.LinkTokenInterface(_link_token.address)
    txn = link_token.transfer(_contract_address, _amount, {"from": account})
    txn.wait(1)
    print(f"LINK Tokens transferred. Contract funded!")
    # return txn

def get_logo(logo_number):
    return LOGO_MAPPING[logo_number]

def upload_to_ipfs(_filepath):
    with Path(_filepath).open("rb") as fpath:
        image_binary = fpath.read()
        ipfs_url = "http://127.0.0.1:5001"
        end_point = "/api/v0/add"
        response = requests.post(ipfs_url + end_point, files={"file": image_binary})
        print(f"Response.JSON: {response.json()}")
        # requests.post returns 4 parameters, of which we only need "Hash"
        ipfs_hash = response.json()["Hash"]
        # filepath has the entire path, of which we only need fileNAME
        # e.g. "./img/igx_white" will be split by "/" and the fileNAME extracted
        filename = _filepath.split("/")[-1:][0]
        fileURI = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
        print(f"Image URI = {fileURI}")

def upload_to_pinata(_filepath):
    with Path(_filepath).open("rb") as fpath:
        image_binary = fpath.read()
        # Get PINATA API key and API secret key from .env
        pinata_base_url = "https://app.pinata.cloud"
        pinata_file_endpoint = "/pinning/pinFileToIPFS"
        filename = _filepath.split("/")[-1:][0]
        file_headers = {"pinata_api_key": os.getenv("PINATA_API_KEY"), "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),}
        print(f"{file_headers}")
        response = requests.post(
            pinata_base_url + pinata_file_endpoint,
            files={"file": (filename, image_binary)},
            headers=file_headers,
            )
        print(f"Response.JSON: {response.json()}")