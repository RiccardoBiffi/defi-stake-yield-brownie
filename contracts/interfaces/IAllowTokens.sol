// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IAllowTokens {
    function addAllowedToken(address _token) external;

    function removeAllowedToken(address _token) external;

    function isTokenAllowed(address _token) external view returns (bool);
}
