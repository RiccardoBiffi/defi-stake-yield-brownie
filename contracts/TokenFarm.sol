// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "./AllowTokens.sol";

contract TokenFarm is AllowTokens {
    struct Stake {
        address token;
        uint256 amount;
        uint256 lastWithdrawTime;
    }

    // info APR expressed with 2 decimals
    // es: 17,81% -> 1781
    uint256 public APR;
    IERC20 public rewardToken;
    address[] public stakers;
    mapping(address => Stake[]) public staker_stakes;
    mapping(address => uint256) public staker_distinctTokenNumber;
    mapping(address => mapping(address => uint256)) public token_staker_amount;
    mapping(address => address) public token_priceFeed;

    constructor(address _rewardToken) {
        rewardToken = IERC20(_rewardToken);
        APR = 1500; // 15%
    }

    function stakeTokens(uint256 _amount, address _token) public {
        require(_amount > 0, "Amount must be more than 0 tokens");
        require(
            isTokenAllowed(_token),
            "Token not allowed on the platform yet"
        );

        if (staker_distinctTokenNumber[msg.sender] == 0) {
            stakers.push(msg.sender);
        }
        updatedistinctTokensStaked(msg.sender, _token);
        Stake memory stake = Stake(_token, _amount, block.timestamp);
        staker_stakes[msg.sender].push(stake);
        token_staker_amount[_token][msg.sender] += _amount;

        IERC20(_token).transferFrom(msg.sender, address(this), _amount);
    }

    function unstakeTokenAndWithdrawMyReward(address _token) public {
        require(
            isTokenAllowed(_token),
            "Token doesn't exists on the platform yet"
        );
        uint256 balance = token_staker_amount[_token][msg.sender];
        require(balance > 0, "Staked balance is zero");

        withdrawMyReward();
        token_staker_amount[_token][msg.sender] = 0;
        staker_distinctTokenNumber[msg.sender]--;
        maybeRemoveMeFromStakers();
        deleteMyTokenStake(_token);

        IERC20(_token).transfer(msg.sender, balance);
    }

    function withdrawMyReward() public {
        uint256 myReward = getUserAccruedReward(msg.sender);
        require(myReward > 0, "You have not accrued enought RWD tokens");

        Stake[] storage myStakes = staker_stakes[msg.sender];
        for (uint256 i = 0; i < myStakes.length; i++) {
            myStakes[i].lastWithdrawTime = block.timestamp;
        }

        rewardToken.transfer(msg.sender, myReward);

        //todo update APR dynamically
        //remainingRWD = rewardToken.balance(address(this));
        //previousRWD = remainingRWD + myReward;
    }

    function setTokenPriceFeed(address token, address priceFeed)
        public
        onlyOwner
    {
        token_priceFeed[token] = priceFeed;
    }

    function setAPR(uint256 newAPR) public onlyOwner {
        APR = newAPR;
    }

    function getUserTVL(address user) public view returns (uint256) {
        if (staker_distinctTokenNumber[user] > 0) {
            uint256 totalValue = 0;

            for (uint256 i = 0; i < allowedTokens.length; i++) {
                address token = allowedTokens[i];
                uint256 amount = token_staker_amount[token][user];
                if (amount > 0) {
                    totalValue += getUserTokenValue(amount, token);
                }
            }
            return totalValue;
        } else return 0;
    }

    function getUserAccruedReward(address user) public view returns (uint256) {
        if (staker_distinctTokenNumber[user] > 0) {
            uint256 totalReward = 0;

            Stake[] memory myStake = staker_stakes[user];
            for (uint256 i = 0; i < myStake.length; i++) {
                uint256 stakeAnnualValue = 0;
                uint256 accruedValue = 0;
                address token = myStake[i].token;
                uint256 amount = myStake[i].amount;
                uint256 stakeTime = myStake[i].lastWithdrawTime;

                uint256 tvlStake = getUserTokenValue(amount, token);
                stakeAnnualValue = (tvlStake * APR) / 10**4;

                uint256 year = 365 days;
                uint256 timeSinceStake = block.timestamp - stakeTime;
                uint256 accruedSoFarPercent = (timeSinceStake * 10**9) / year;

                accruedValue = (stakeAnnualValue * accruedSoFarPercent) / 10**9;
                totalReward += getTokenFromValue(
                    accruedValue,
                    address(rewardToken)
                );
            }
            return totalReward;
        } else return 0;
    }

    function getUserTokenValue(uint256 amount, address token)
        public
        view
        returns (uint256)
    {
        (uint256 price, uint256 decimals) = getTokenValue(token);
        return (amount * price) / 10**(decimals);
    }

    function getTokenFromValue(uint256 amount, address token)
        public
        view
        returns (uint256)
    {
        (uint256 price, uint256 decimals) = getTokenValue(token);
        return (amount * 10**decimals) / price;
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

    function updatedistinctTokensStaked(address user, address token) internal {
        if (token_staker_amount[token][user] <= 0) {
            staker_distinctTokenNumber[user] += 1;
        }
    }

    function deleteMyTokenStake(address _token) internal {
        Stake[] storage myStakes = staker_stakes[msg.sender];
        for (uint16 i = 0; i < myStakes.length; i++) {
            if (myStakes[i].token == _token) {
                myStakes[i] = myStakes[myStakes.length - 1];
                myStakes.pop();
            }
        }
    }

    function maybeRemoveMeFromStakers() internal {
        if (staker_distinctTokenNumber[msg.sender] == 0) {
            for (uint256 i = 0; i < stakers.length; i++) {
                if (stakers[i] == msg.sender) {
                    stakers[i] = stakers[stakers.length - 1];
                    stakers.pop();
                    break;
                }
            }
        }
    }
}
