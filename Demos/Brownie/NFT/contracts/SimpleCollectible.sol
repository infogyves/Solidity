//SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";

contract SimpleCollectible is ERC721URIStorage {
    uint256 public tokenCounter;

    constructor() public ERC721URIStorage("Infogyves", "IGX") {
        tokenCounter = 0;
    }

    function createCollectibe(string memory tokenURI) public returns (uint256) {
        uint256 newTokenID = tokenCounter;
        _safeMint(msg.sender, newTokenID);
        _setTokenURI(newTokenID, tokenURI);
        tokenCounter = tokenCounter + 1;
        return newTokenID;
    }
}
