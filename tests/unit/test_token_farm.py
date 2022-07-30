from brownie import TokenFarm, RewardToken
from brownie import network, exceptions
import pytest
from scripts.utilities import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def test_can_deploy_token_farm():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    rewardToken = "0x7777cBDC3dbcd3E11a07892e7bA5c33940487777"

    # Act
    tf = TokenFarm.deploy(rewardToken, {"from": account})

    # Assert
    assert tf.address != None


def test_can_allow_tokens():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_addr = "0x4194cBDC3dbcd3E11a07892e7bA5c3394048Cc87"
    rewardToken = "0x7777cBDC3dbcd3E11a07892e7bA5c33940487777"

    # Act
    tf = TokenFarm.deploy(rewardToken, {"from": account})
    tf.addAllowedToken(token_addr, {"from": account})

    # Assert
    assert tf.allowedTokens(0) == "0x4194cBDC3dbcd3E11a07892e7bA5c3394048Cc87"


def test_check_token_allowed_true():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_addr = "0x4194cBDC3dbcd3E11a07892e7bA5c3394048Cc87"
    rewardToken = "0x7777cBDC3dbcd3E11a07892e7bA5c33940487777"

    tf = TokenFarm.deploy(rewardToken, {"from": account})
    tf.addAllowedToken(token_addr, {"from": account})

    # Act
    answer = tf.isTokenAllowed(token_addr, {"from": account})

    # Assert
    assert answer == True


def test_check_token_allowed_false():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_addr = "0x4194cBDC3dbcd3E11a07892e7bA5c3394048Cc87"
    rewardToken = "0x7777cBDC3dbcd3E11a07892e7bA5c33940487777"
    other_token_addr = "0x9294cBDC3dbcd3E11a07892e7bA5c3394048Cc51"
    tf = TokenFarm.deploy(rewardToken, {"from": account})
    tf.addAllowedToken(token_addr, {"from": account})

    # Act
    answer = tf.isTokenAllowed(other_token_addr, {"from": account})

    # Assert
    assert answer == False


def test_stake_token_success():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    amount = 10**18
    rewardToken = "0x4194CBDC3DBCD3E11A07892E7BA5C3394048CC87"
    token = RewardToken.deploy(10, {"from": account})
    tf = TokenFarm.deploy(rewardToken, {"from": account})

    token.approve(tf.address, amount, {"from": account})
    tf.addAllowedToken(token.address, {"from": account})

    # Act
    tf.stakeTokens(amount, token.address, {"from": account})

    # Assert
    assert tf.token_staker_amount(token.address, account) == amount
    assert tf.stakers(0) == account
    assert tf.staker_uniqueTokenNumber(account) == 1
    assert token.balanceOf(tf.address) == amount


def test_stake_token_fail_low_amount():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_addr = "0x4194cBDC3dbcd3E11a07892e7bA5c3394048Cc87"
    rewardToken = "0x7777cBDC3dbcd3E11a07892e7bA5c33940487777"
    tf = TokenFarm.deploy(rewardToken, {"from": account})

    # Act

    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        tf.stakeTokens(0, token_addr, {"from": account})


def test_stake_token_fail_not_allowed():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_addr = "0x4194cBDC3dbcd3E11a07892e7bA5c3394048Cc87"
    rewardToken = "0x7777cBDC3dbcd3E11a07892e7bA5c33940487777"
    tf = TokenFarm.deploy(rewardToken, {"from": account})

    # Act

    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        tf.stakeTokens(10**18, token_addr, {"from": account})


def test_set_token_price_feed_success():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    account = get_account()
    token_addr = "0x4194cBDC3dbcd3E11a07892e7bA5c3394048Cc87"
    rewardToken = "0x7777cBDC3dbcd3E11a07892e7bA5c33940487777"
    price_feed_addr = "0x9999cBDC3dbcd3E11a07892e7bA5c33940489999"
    tf = TokenFarm.deploy(rewardToken, {"from": account})

    # Act
    tf.setTokenPriceFeed(token_addr, price_feed_addr, {"from": account})

    # Assert
    assert tf.token_priceFeed(token_addr) == price_feed_addr


def test_set_token_price_feed_fail_no_owner():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local testing")

    # Arrange
    admin = get_account()
    user = get_account(1)
    token_addr = "0x4194cBDC3dbcd3E11a07892e7bA5c3394048Cc87"
    rewardToken = "0x7777cBDC3dbcd3E11a07892e7bA5c33940487777"
    price_feed_addr = "0x9999cBDC3dbcd3E11a07892e7bA5c33940489999"
    tf = TokenFarm.deploy(rewardToken, {"from": admin})

    # Act

    # Assert
    with pytest.raises(exceptions.VirtualMachineError):
        tf.setTokenPriceFeed(token_addr, price_feed_addr, {"from": user})
