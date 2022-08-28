// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract RewardToken is ERC20, Ownable {
    address[] public allowedTokens;
    mapping(address => address) public token_priceFeed;

    constructor(uint256 initialSupply) ERC20("Reward", "RWD") {
        _mint(msg.sender, initialSupply);
    }

    function buy(uint256 amount, address exchangeToken) public {
        IERC20(exchangeToken).transferFrom(msg.sender, address(this), amount);
        // compute RWD value
        uint256 buyedTokens = 10**18;
        transfer(msg.sender, buyedTokens);
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

    function setTokenPriceFeed(address token, address priceFeed)
        public
        onlyOwner
    {
        token_priceFeed[token] = priceFeed;
    }
}
