//SPDX-License-Identifier: MIT

pragma solidity ^0.6.9;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

//import "@chainlink/contracts/src/v0.8/VRFConsumerBaseV2.sol";

// import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract Lottery is VRFConsumerBase, Ownable {
    // List of participants or "players"
    address payable[] public players;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    // Enumerated lottery state of 0, 1, 2
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;
    uint256 public fee;
    bytes32 public keyhash;
    uint256 public randomness;
    address payable public recentWinner;

    constructor(
        address _pPriceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        // Minimum is $50, converted to Wei
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_pPriceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
    }

    // Participants or "players" will need to pay to play
    function enter() public payable {
        // Lottery state needs to be open!
        require(
            lottery_state == LOTTERY_STATE.OPEN,
            "Lottery is not open yet!"
        );
        // Minimum is $50
        require(
            msg.value >= getEntranceFees(),
            "Not enough ETH to participate in this Lottery!"
        );
        players.push(msg.sender);
    }

    function getEntranceFees() public view returns (uint256) {
        (
            ,
            /*uint80 roundID*/
            int256 price, /*uint startedAt*/ /*uint timeStamp*/
            ,
            ,

        ) = ethUsdPriceFeed.latestRoundData();
        // Convert "price" to uint256
        uint256 adjustedPrice = uint256(price) * (10**10); // 18 decimal places for Wei
        uint256 costToEnter = (usdEntryFee * (10**18)) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "A lottery is already running. Cannot start a new lottery!"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        // Set the lottery state to "calculating winner".
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        // Request a random number...
        // This is a request/response type structure
        // requestRandomness will call fulfillRandomness defined later
        bytes32 requestId = requestRandomness(keyhash, fee);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        // Check if lottery is in CORRECT state:
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "Lottery is still running. Not there yet!"
        );
        // Ensure random number has ACUTALLY been generated:
        require(_randomness > 0, "random-not-found Error!");
        // Use random number to select a lottery winner!
        uint256 indexOfWinner = _randomness % players.length;
        recentWinner = players[indexOfWinner];
        // Pay the winner ALL of the lottery money!
        recentWinner.transfer(address(this).balance);
        // DONE!!!!
        // Now reset everything so we can startover:
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }
}
