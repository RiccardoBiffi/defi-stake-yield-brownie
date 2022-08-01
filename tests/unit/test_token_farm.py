from brownie import network, exceptions
import pytest
from scripts.utilities import (
    MockContract,
    get_account,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_contract,
    DECIMALS,
)
from scripts.deploy import deploy_token_farm_and_dapp_token


def test_can_deploy_token_farm():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange

    # Act
    token_farm, _ = deploy_token_farm_and_dapp_token()

    # Assert
    assert token_farm.address != None


# region stakeTokens
def test_stake_token_success(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, reward_token = deploy_token_farm_and_dapp_token()
    previous_balance = reward_token.balanceOf(token_farm.address)

    # Act
    reward_token.approve(token_farm.address, amount_staked, {"from": account})
    token_farm.stakeTokens(amount_staked, reward_token.address, {"from": account})

    # Assert
    assert (
        token_farm.token_staker_amount(reward_token.address, account) == amount_staked
    )
    assert token_farm.stakers(0) == account
    assert token_farm.staker_uniqueTokenNumber(account) == 1
    assert (
        reward_token.balanceOf(token_farm.address) - previous_balance == amount_staked
    )
    return token_farm, reward_token


def test_stake_token_fail_low_amount(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, reward_token = deploy_token_farm_and_dapp_token()

    # Act
    reward_token.approve(token_farm.address, amount_staked, {"from": account})

    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.stakeTokens(0, reward_token.address, {"from": account})


def test_stake_token_fail_not_allowed(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, reward_token = deploy_token_farm_and_dapp_token()
    not_allowed_token = "0x4194cBDC3dbcd3E11a07892e7bA5c3394048Cc87"

    # Act
    reward_token.approve(token_farm.address, amount_staked, {"from": account})

    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.stakeTokens(10**18, not_allowed_token, {"from": account})


# endregion

# region unstakeTokens
def test_unstake_token_success(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, reward_token = test_stake_token_success(amount_staked)
    previous_balance = reward_token.balanceOf(account)

    # Act
    token_farm.unstakeTokens(reward_token.address, {"from": account})

    # Assert
    assert reward_token.balanceOf(account) == previous_balance + amount_staked
    assert token_farm.token_staker_amount(reward_token.address, account) == 0
    assert token_farm.staker_uniqueTokenNumber(account) == 0
    # hack check for empty stakers array
    with pytest.raises(exceptions.VirtualMachineError):
        assert token_farm.stakers(0)


def test_unstake_token_fail_not_allowed():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    not_allowed_token = "0x4194cBDC3dbcd3E11a07892e7bA5c3394048Cc87"
    token_farm, _ = deploy_token_farm_and_dapp_token()

    # Act

    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.unstakeTokens(not_allowed_token, {"from": account})


def test_unstake_token_fail_zero_balance():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, reward_token = deploy_token_farm_and_dapp_token()

    # Act

    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.unstakeTokens(reward_token, {"from": account})


# endregion

# region issueRerwardTokens
def test_issue_reward_tokens_success(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, reward_token = test_stake_token_success(amount_staked)
    starting_balance = reward_token.balanceOf(account)

    # Act
    token_farm.issueRewardTokens({"from": account})

    # Assert
    assert reward_token.balanceOf(account) == starting_balance + 10**DECIMALS


def test_issue_reward_tokens_fail_no_owner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    not_owner = get_account(1)
    token_farm, _ = deploy_token_farm_and_dapp_token()

    # Act

    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.issueRewardTokens({"from": not_owner})


# endregion


def test_add_allowed_tokens():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, reward_token = deploy_token_farm_and_dapp_token()
    token_farm.addAllowedToken(reward_token.address, {"from": account})

    # Act

    # Assert
    assert token_farm.allowedTokens(0) == reward_token.address


# region isTokenAllowed
def test_check_token_allowed_true():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, reward_token = deploy_token_farm_and_dapp_token()
    token_farm.addAllowedToken(reward_token.address, {"from": account})

    # Act
    answer = token_farm.isTokenAllowed(reward_token, {"from": account})

    # Assert
    assert answer == True


def test_check_token_allowed_false():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, reward_token = deploy_token_farm_and_dapp_token()
    not_allowed_token = "0x4194cBDC3dbcd3E11a07892e7bA5c3394048Cc87"
    token_farm.addAllowedToken(reward_token.address, {"from": account})

    # Act
    answer = token_farm.isTokenAllowed(not_allowed_token, {"from": account})

    # Assert
    assert answer == False


# endregion

# region setTokenPriceFeed
def test_set_token_price_feed_success():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, reward_token = deploy_token_farm_and_dapp_token()
    price_feed_addr = get_contract(MockContract.ETH_USD_FEED)

    # Act
    token_farm.setTokenPriceFeed(
        reward_token.address, price_feed_addr, {"from": account}
    )

    # Assert
    assert token_farm.token_priceFeed(reward_token.address) == price_feed_addr


def test_set_token_price_feed_fail_no_owner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    not_owner = get_account(1)
    token_farm, reward_token = deploy_token_farm_and_dapp_token()
    price_feed_addr = get_contract(MockContract.ETH_USD_FEED)

    # Act

    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setTokenPriceFeed(
            reward_token.address, price_feed_addr, {"from": not_owner}
        )


# endregion

# region getUserTVL
def test_get_user_tvl_success(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, _ = test_stake_token_success(amount_staked)

    # Act
    tvl = token_farm.getUserTVL(account.address, {"from": account})

    # Assert
    assert tvl == 10**DECIMALS


def test_set_token_price_feed_fail_no_owner(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    no_owner = get_account(1)
    token_farm, _ = test_stake_token_success(amount_staked)

    # Act

    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.getUserTVL(no_owner.address, {"from": account})


# endregion


def test_get_user_token_value(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, reward_token = test_stake_token_success(amount_staked)

    # Act
    tvl = token_farm.getUserTokenValue(amount_staked, reward_token, {"from": account})

    # Assert
    assert tvl == 10**DECIMALS


def test_get_token_value():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, reward_token = deploy_token_farm_and_dapp_token()

    # Act
    tv = token_farm.getTokenValue(reward_token, {"from": account})

    # Assert
    assert tv == (10**DECIMALS, DECIMALS)
