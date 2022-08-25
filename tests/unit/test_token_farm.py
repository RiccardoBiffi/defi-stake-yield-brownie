from brownie import network, exceptions, chain
import pytest
from web3 import Web3
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
    tx = token_farm.stakeTokens(amount_staked, reward_token.address, {"from": account})
    (token, amount, _) = token_farm.staker_stakes(account.address, 0)

    # Assert
    assert token_farm.stakers(0) == account
    assert token_farm.staker_distinctTokenNumber(account) == 1
    assert (token, amount, _) == (reward_token.address, amount_staked, _)
    assert (
        token_farm.token_staker_amount(reward_token.address, account) == amount_staked
    )
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
    chain.sleep(1000)
    chain.mine(1)
    reward = token_farm.getUserAccruedReward(account, {"from": account})
    previous_balance = reward_token.balanceOf(account)

    # Act
    token_farm.unstakeTokenAndWithdrawMyReward(reward_token.address, {"from": account})

    # Assert
    assert reward_token.balanceOf(account) == previous_balance + amount_staked + reward
    assert token_farm.token_staker_amount(reward_token.address, account) == 0
    assert token_farm.staker_distinctTokenNumber(account) == 0
    # hack check for empty myStakes array
    with pytest.raises(exceptions.VirtualMachineError):
        assert token_farm.staker_stakes(account.address, 0)
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
        token_farm.unstakeTokenAndWithdrawMyReward(not_allowed_token, {"from": account})


def test_unstake_token_fail_zero_balance():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, reward_token = deploy_token_farm_and_dapp_token()

    # Act

    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.unstakeTokenAndWithdrawMyReward(reward_token, {"from": account})


# endregion

# region issueRerwardTokens
def test_withdraw_my_reward_success(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, reward_token = test_stake_token_success(amount_staked)
    starting_balance = reward_token.balanceOf(account)
    chain.sleep(1000)
    chain.mine(1)
    reward = token_farm.getUserAccruedReward(account, {"from": account})

    # Act
    token_farm.withdrawMyReward({"from": account})

    # Assert
    assert reward_token.balanceOf(account) == starting_balance + reward


def test_withdraw_my_reward_fail_not_enought():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, _ = deploy_token_farm_and_dapp_token()

    # Act

    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.withdrawMyReward({"from": account})


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
def test_get_user_tvl_more_than_zero(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, _ = test_stake_token_success(amount_staked)

    # Act
    tvl = token_farm.getUserTVL(account, {"from": account})

    # Assert
    assert tvl == 10**DECIMALS


def test_get_user_tvl_zero():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, _ = deploy_token_farm_and_dapp_token()

    # Act
    tvl = token_farm.getUserTVL(account, {"from": account})

    # Assert
    assert tvl == 0


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


def test_get_token_from_value():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, reward_token = deploy_token_farm_and_dapp_token()
    amount = Web3.toWei(1, "ether")

    # Act
    tfv = token_farm.getTokenFromValue(amount, reward_token, {"from": account})

    # Assert
    assert tfv == 10**DECIMALS


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


def test_get_user_accrued_reward_zero():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, _ = deploy_token_farm_and_dapp_token()

    # Act
    ar = token_farm.getUserAccruedReward(account, {"from": account})

    # Assert
    assert ar == 0


def test_get_user_accrued_reward_more_than_zero(amount_staked):
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, _ = test_stake_token_success(amount_staked)
    chain.sleep(1000)
    chain.mine(1)

    # Act
    ar = token_farm.getUserAccruedReward(account, {"from": account})

    # Assert
    assert ar > 0


def test_set_APR_success():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_farm, _ = deploy_token_farm_and_dapp_token()
    new_APR = 2000

    # Act
    token_farm.setAPR(new_APR, {"from": account})

    # Assert
    assert token_farm.APR() == new_APR


def test_set_APR_fail_not_owner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    not_owner = get_account(1)
    token_farm, _ = deploy_token_farm_and_dapp_token()
    new_APR = 2000

    # Act

    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setAPR(new_APR, {"from": not_owner})
