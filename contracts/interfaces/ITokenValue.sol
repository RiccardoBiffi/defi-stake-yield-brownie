// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface ITokenValue {
    function setTokenPriceFeed(address token, address priceFeed) external;

    function getValueFromToken(uint256 amount, address token)
        external
        view
        returns (uint256);

    function getTokenFromValue(uint256 amount, address token)
        external
        view
        returns (uint256);

    function getTokenValue(address token)
        external
        view
        returns (uint256, uint256);
}
