// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "./AllowTokens.sol";
import "./TokenValue.sol";

contract RewardToken is ERC20, AllowTokens, TokenValue {
    address[] public tokenWithDeposits;
    mapping(address => uint256) public token_deposit;

    event Exchange(
        address from,
        address exchangeToken,
        uint256 amountIn,
        uint256 amountRwdOut
    );
    event CashOut(address admin);

    constructor(uint256 initialSupply) ERC20("Reward", "RWD") {
        _mint(msg.sender, initialSupply);
    }

    function buy(uint256 amount, address exchangeToken) public {
        IERC20(exchangeToken).transferFrom(msg.sender, address(this), amount);
        tokenWithDeposits.push(exchangeToken);
        token_deposit[exchangeToken] = amount;

        uint256 valueSent = getValueFromToken(amount, exchangeToken);
        uint256 buyedRwdTokens = getTokenFromValue(valueSent, address(this));
        transfer(msg.sender, buyedRwdTokens);

        emit Exchange(msg.sender, exchangeToken, amount, buyedRwdTokens);
    }

    function cashOut() public onlyOwner {
        for (uint256 i = 0; i < tokenWithDeposits.length; i++) {
            IERC20(tokenWithDeposits[i]).transfer(
                owner(),
                token_deposit[tokenWithDeposits[i]]
            );
            delete token_deposit[tokenWithDeposits[i]];
        }

        delete tokenWithDeposits;
        emit CashOut(msg.sender);
    }

    function setTokenPriceFeed(address token, address priceFeed)
        public
        override
        onlyOwner
    {
        super.setTokenPriceFeed(token, priceFeed);
    }
}
