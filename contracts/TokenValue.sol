// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "./interfaces/ITokenValue.sol";

contract TokenValue is ITokenValue {
    mapping(address => address) public token_priceFeed;

    event AddedPriceFeed(address admin, address token, address priceFeed);
    event RemovedPriceFeed(address admin, address token);

    function setTokenPriceFeed(address token, address priceFeed)
        public
        virtual
        override
    {
        token_priceFeed[token] = priceFeed;
        emit AddedPriceFeed(msg.sender, token, priceFeed);
    }

    function removeTokenPriceFeed(address token) public virtual override {
        delete token_priceFeed[token];
        emit RemovedPriceFeed(msg.sender, token);
    }

    function getValueFromToken(uint256 amount, address token)
        public
        view
        override
        returns (uint256)
    {
        (uint256 price, uint256 decimals) = getTokenValue(token);
        return (amount * price) / 10**(decimals);
    }

    function getTokenFromValue(uint256 amount, address token)
        public
        view
        override
        returns (uint256)
    {
        (uint256 price, uint256 decimals) = getTokenValue(token);
        return (amount * 10**decimals) / price;
    }

    function getTokenValue(address token)
        public
        view
        override
        returns (uint256, uint256)
    {
        address tokenPriceFeed = token_priceFeed[token];
        AggregatorV3Interface priceFeed = AggregatorV3Interface(tokenPriceFeed);

        (, int256 price, , , ) = priceFeed.latestRoundData();
        uint256 decimals = priceFeed.decimals();

        return (uint256(price), decimals);
    }
}
