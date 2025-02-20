//SPDX-License-Identifier: MIT

pragma solidity >=0.6.6 <=0.9.0;

import {AggregatorV3Interface} from "@chainlink/contracts/src/v0.8/shared/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) public addressToAmount;
    address owner;
    address[] funders;
    AggregatorV3Interface public priceFeed;
    //uint256 public minAmt;

    constructor(address _pricefeed) {
        priceFeed = AggregatorV3Interface(_pricefeed);
        owner = msg.sender;
    }
    /*
    function minGwei() public {
        uint256 ethPrice = getPrice() / 1000000000000000000;
        //Min amount is $50
        uint256 divisorAmount = ethPrice / 50;
        minAmt = (1 / divisorAmount) * 10 ** 9;
    }

    function minAmount() public view returns (uint256) {
        return minAmt;
    }
    */
    function fund() public payable {
        uint256 minUsd = 50 * 10 ** 18;
        require(
            getCOnversionRate(msg.value) >= minUsd,
            "You need to send atleast $50"
        );
        addressToAmount[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    function getCOnversionRate(
        uint256 ethAmount
    ) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 getAmountInUsd = (ethAmount * ethPrice) / 1000000000000000000;
        return getAmountInUsd;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only Owner can withdraw!");
        _;
    }

    function withdraw() public payable onlyOwner {
        address payable to = payable(msg.sender);
        to.transfer(address(this).balance);
        for (uint256 i = 0; i < funders.length; i++) {
            address funder = funders[i];
            addressToAmount[funder] = 0;
        }
        funders = new address[](0);
    }

    function getEntranceFee() public view returns (uint256) {
        //minUSD
        uint256 minimumUSD = 50 * 10 ** 18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10 ** 18;
        return (minimumUSD * precision) / price;
    }
}
