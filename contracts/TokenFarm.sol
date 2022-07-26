// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract TokenFarm is Ownable {
    IERC20 public rewardToken;
    address[] public allowedTokens;
    address[] public stakers;
    mapping(address => mapping(address => uint256)) public token_staker_amount;
    mapping(address => uint256) public staker_uniqueTokenNumber;

    constructor(address _rewardToken) {
        rewardToken = IERC20(_rewardToken);
    }

    function stakeTokens(uint256 _amount, address _token) public {
        require(_amount > 0, "Amount must be more than 0 tokens");
        require(
            isTokenAllowed(_token),
            "Token not allowed on the platform yet"
        );

        token_staker_amount[_token][msg.sender] += _amount;
        if (staker_uniqueTokenNumber[msg.sender] == 0) {
            stakers.push(msg.sender);
        }
        updateUniqueTokensStaked(msg.sender, _token);

        IERC20(_token).transferFrom(msg.sender, address(this), _amount);
    }

    // issue dapp token for all stakers
    function issueRewardTokens() public onlyOwner {
        for (uint256 i = 0; i < stakers.length; i++) {
            address recipient = stakers[i];
            // todo send a token reward depending on token combination owned
            // i'll need to convert all staked token to a common denominator
            // that is the TVL!
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

    // update the number of unique tokens owned by user
    function updateUniqueTokensStaked(address user, address token) internal {
        if (token_staker_amount[token][user] <= 0) {
            staker_uniqueTokenNumber[user] += 1;
        }
    }
}
