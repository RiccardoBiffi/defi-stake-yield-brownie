// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract TokenFarm is Ownable {
    IERC20 public rewardToken;
    address[] public allowedTokens;
    address[] public stakers;
    mapping(address => mapping(address => uint256)) public token_staker_amount;
    mapping(address => uint256) public staker_uniqueTokenNumber;
    mapping(address => address) public token_priceFeed;

    constructor(address _rewardToken) {
        rewardToken = IERC20(_rewardToken);
    }

    function stakeTokens(uint256 _amount, address _token) public {
        require(_amount > 0, "Amount must be more than 0 tokens");
        require(
            isTokenAllowed(_token),
            "Token not allowed on the platform yet"
        );

        if (staker_uniqueTokenNumber[msg.sender] == 0) {
            stakers.push(msg.sender);
        }
        updateUniqueTokensStaked(msg.sender, _token);
        token_staker_amount[_token][msg.sender] += _amount;

        IERC20(_token).transferFrom(msg.sender, address(this), _amount);
    }

    function unstakeTokens(address _token) public {
        // security is vulnerable to reentrancy attacks?
        require(
            isTokenAllowed(_token),
            "Token doesn't exists on the platform yet"
        );
        uint256 balance = token_staker_amount[_token][msg.sender];
        require(balance > 0, "staked balance is zero");
        IERC20(_token).transfer(msg.sender, balance);
        token_staker_amount[_token][msg.sender] = 0;
        staker_uniqueTokenNumber[msg.sender]--;

        if (staker_uniqueTokenNumber[msg.sender] == 0) {
            for (uint256 i = 0; i < stakers.length; i++) {
                if (stakers[i] == msg.sender) {
                    stakers[i] = stakers[stakers.length - 1];
                    stakers.pop();
                    break;
                }
            }
        }
    }

    // issue dapp token for all stakers
    function issueRewardTokens() public onlyOwner {
        for (uint256 i = 0; i < stakers.length; i++) {
            address recipient = stakers[i];
            uint256 user_TVL = getUserTVL(msg.sender);

            // info here you can modify the issuance logic
            rewardToken.transfer(recipient, user_TVL);
        }
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

    function getUserTVL(address _user) public view returns (uint256) {
        require(staker_uniqueTokenNumber[_user] > 0, "No tokens staked");
        uint256 totalValue = 0;

        for (uint256 i = 0; i < allowedTokens.length; i++) {
            address token = allowedTokens[i];
            uint256 amount = token_staker_amount[token][_user];
            if (amount > 0) {
                totalValue += getUserTokenValue(amount, token);
            }
        }
        return totalValue;
    }

    function getUserTokenValue(uint256 amount, address token)
        public
        view
        returns (uint256)
    {
        (uint256 price, uint256 decimals) = getTokenValue(token);
        return (amount * price) / 10**decimals;
    }

    function getTokenValue(address token)
        public
        view
        returns (uint256, uint256)
    {
        address tokenPriceFeed = token_priceFeed[token];
        AggregatorV3Interface priceFeed = AggregatorV3Interface(tokenPriceFeed);

        (, int256 price, , , ) = priceFeed.latestRoundData();
        uint256 decimals = priceFeed.decimals();

        return (uint256(price), decimals);
    }

    function updateUniqueTokensStaked(address user, address token) internal {
        if (token_staker_amount[token][user] <= 0) {
            staker_uniqueTokenNumber[user] += 1;
        }
    }
}
