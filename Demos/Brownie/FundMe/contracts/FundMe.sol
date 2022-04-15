// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256;
    mapping(address => uint256) public simpleAddresstoFundAmount;
    AggregatorV3Interface public priceFeed;
    address[] public funders;
    address public contractOwner;

    constructor(address _priceFeed) public {
        contractOwner = msg.sender;
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    function simpleFund() public payable {
        // But this is all in ETH...
        // What is the ETH -> USD conversion rate?
        // 1. Get the ETH->USD Rate
        // 2. Convert ETH to USD using the rate
        // 3. Compare with $50 and revert, if not eligible
        // uint256 minimumFund = 50 * 10 ** 18;
        uint256 minimumFund = 50;
        require(
            getUsdAmount(msg.value) >= minimumFund,
            "You need to spend more ETH!"
        );
        simpleAddresstoFundAmount[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getFeedVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getUsdRate() public view returns (uint256) {
        // This it the getPrice function in Patrick's example
        // and returns USD Rate in Gwei
        (
            ,
            /*uint80 roundID*/
            int256 latestUsdPrice, /*uint startedAt*/ /*uint timeStamp*/ /*uint80 answeredInRound*/
            ,
            ,

        ) = priceFeed.latestRoundData();
        return uint256(latestUsdPrice * 10000000000);
    }

    function getUsdAmount(uint256 _pEthAmount) public view returns (uint256) {
        // This is the getConversionRate function in Patrick's example
        // It actually returns the total amount in USD
        // get USD Amount for ETH
        uint256 currentUsdRate = getUsdRate();
        //get USD total by multiplying with ETH
        uint256 valueEthInUSD = (currentUsdRate * _pEthAmount) /
            1000000000000000000;
        return valueEthInUSD;
    }

    function getUsdEntranceFee() public view returns (uint256) {
        uint256 minimumUsd = 50 * 10**18;
        uint256 rateUsd = getUsdRate();
        uint256 precision = 1 * 10**18;
        return ((minimumUsd * precision) / rateUsd) + 1;
    }

    modifier onlyOwner() {
        require(msg.sender == contractOwner);
        _;
    }

    function simpleWithdraw() public payable onlyOwner {
        msg.sender.transfer(address(this).balance);
        for (
            uint256 fundersIndex = 0;
            fundersIndex < funders.length;
            fundersIndex++
        ) {
            address funder = funders[fundersIndex];
            simpleAddresstoFundAmount[funder] = 0;
        }
        // Reset Funders array
        funders = new address[](0);
    }
}
