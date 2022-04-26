// A NFT contract
// Where the tokenURI could be ONE OF THREE images
// Randomly selected

// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

// Import ERC721 contract
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
// Import VRF Consumer Base to create provably random numbers
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {

    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    enum Logo {BLACK, WHITE, COLOUR}
    mapping(uint256 => Logo) public tokenIDToLogo;
    event logoAssigned(uint256 indexed tokenID, Logo logoChoice);
    mapping(bytes32 => address) public requestIDToSender;
    event requestedCollectible(bytes32 indexed requestID, address requester);

    constructor(address _VRFCoordinator, address _linkToken, bytes32 _keyhash, uint256 _fee) public 
    VRFConsumerBase(_VRFCoordinator, _linkToken)
    ERC721("Infogyves", "IGX") {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestID = requestRandomness(keyhash, fee);
        requestIDToSender[requestID] = msg.sender;
        emit requestedCollectible(requestID, msg.sender);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomNumber) internal override {
        Logo logo_choice = Logo(_randomNumber % 3);
        uint256 newTokenID = tokenCounter;
        tokenIDToLogo[newTokenID] = logo_choice;
        emit logoAssigned(newTokenID, logo_choice);
        address sender = requestIDToSender[_requestId];
        _safeMint(sender, newTokenID);
        // _setTokenURI(newTokenID, tokenURI);
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 _tokenID, string memory _tokenURI) public {
        // Check if it's the owner or someone approved, to allow setting URI
        require(_isApprovedOrOwner(_msgSender(), _tokenID), "ERC721: Caller is neither Owner nor approved!");
        _setTokenURI(_tokenID, _tokenURI);
    }
}

