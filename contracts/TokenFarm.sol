// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";

contract TokenFarm is Ownable {
    address[] public allowedTokens;
    uint256 public stakedTokens;

    function stakeTokens(uint256 _amount, address _token) public {
        // what token to stake?
        // how much? > 0
        require(_amount > 0, "You can't stake an amount of 0 tokens");
        require(
            isTokenAllowed(_token),
            "This token is not allowed on the platform"
        );
        stakedTokens += _amount;
    }

    function addAllowedToken(address _token) public onlyOwner {
        allowedTokens.push(_token);
    }

    function isTokenAllowed(address _token) public view returns (bool) {
        for (uint256 i = 0; i < allowedTokens.length; i++) {
            if (allowedTokens[i] == _token) {
                return true;
            }
        }
        return false;
    }
}
