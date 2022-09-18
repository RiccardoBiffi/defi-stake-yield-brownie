// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./interfaces/IAllowTokens.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract AllowTokens is IAllowTokens, Ownable {
    address[] public allowedTokens;

    event AllowToken(address admin, address token);
    event DisallowToken(address admin, address token);

    function addAllowedToken(address token) public override onlyOwner {
        bool exists = false;
        for (uint256 i = 0; i < allowedTokens.length; i++) {
            if (allowedTokens[i] == token) {
                exists = true;
                break;
            }
        }
        require(!exists, "The token is already allowed");

        allowedTokens.push(token);
        emit AllowToken(msg.sender, token);
    }

    function removeAllowedToken(address token) public override onlyOwner {
        uint256 tokenIndex = allowedTokens.length;
        for (uint256 i = 0; i < allowedTokens.length; i++) {
            if (allowedTokens[i] == token) {
                tokenIndex = i;
                break;
            }
        }
        require(
            tokenIndex < allowedTokens.length,
            "The token is already unallowed"
        );

        allowedTokens[tokenIndex] = allowedTokens[allowedTokens.length - 1];
        allowedTokens.pop();
        emit DisallowToken(msg.sender, token);
    }

    function isTokenAllowed(address token) public view override returns (bool) {
        for (uint256 i = 0; i < allowedTokens.length; i++) {
            if (allowedTokens[i] == token) {
                return true;
            }
        }
        return false;
    }
}
