from lib2to3.pgen2 import token
from brownie import AdvancedCollectible, network
from scripts.igx_library import get_logo, upload_to_ipfs, upload_to_pinata
from metadata.sample_metadata import metadata_template
from pathlib import Path

def create_collectible_metadata():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_collectibles = advanced_collectible.tokenCounter()
    print(f"You have created {number_of_advanced_collectibles} collectibles!!!")
    for token_ID in range(number_of_advanced_collectibles):
        logo = get_logo(advanced_collectible.tokenIDToLogo(token_ID))
        metadata_file_name = f"./metadata/{network.show_active()}/{token_ID}-{logo}.json"
        print(f"{metadata_file_name}")
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"Metadata file {metadata_file_name} already exists! Delete it to create a new one!")
        else:
            print(f"Creating Metadata file: {metadata_file_name}")
            collectible_metadata["name"] = logo
            collectible_metadata["description"] = f"A hexagonal symmetrical IGX {logo.capitalize()} NFT Logo"
            print(f"{collectible_metadata}")
            collectible_file_path = "./img/igx_" + logo.lower() + ".png"
            print(f"{collectible_file_path}")
            # upload_to_ipfs(collectible_file_path)
            upload_to_pinata(collectible_file_path)
        




def main():
    create_collectible_metadata()